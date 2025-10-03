<!-- 时间轴头部组件 -->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { formatTime, getCurrentTime } from '@/utils/time'
import dayjs from 'dayjs'

interface Props {
  timelineStart: string
  timelineEnd: string
  pixelsPerHour: number
  scrollLeft?: number
  scrollTop?: number
  currentPageDate?: string
}

const props = withDefaults(defineProps<Props>(), {
  scrollLeft: 0,
  scrollTop: 0
})

const emit = defineEmits<{
  scroll: [value: number]
  'update:pixelsPerHour': [value: number]
}>()

// DOM引用
const timelineRef = ref<HTMLElement>()
const isDragging = ref(false)
const dragStartX = ref(0)
const initialScrollLeft = ref(0)

// 计算属性
const timelineWidth = computed(() => {
  const start = dayjs(props.timelineStart)
  const end = dayjs(props.timelineEnd)
  const totalMinutes = end.diff(start, 'minute')
  return (totalMinutes / 60) * props.pixelsPerHour
})


// 时间刻度 - 支持连续时间轴显示
const timeMarkers = computed(() => {
  const markers = []
  const start = dayjs(props.timelineStart)
  const end = dayjs(props.timelineEnd)
  const totalHours = Math.ceil(end.diff(start, 'hour'))
  
  // 生成小时刻度
  for (let i = 0; i <= totalHours; i++) {
    const time = start.add(i, 'hour')
    const position = (i * props.pixelsPerHour)
    
    // 判断是否是新的一天
    const isNewDay = i === 0 || time.hour() === 0
    const isMajor = i % 4 === 0 || isNewDay
    
    // 判断是否是当前页面日期
    const isCurrentPage = props.currentPageDate ? 
      time.format('YYYY-MM-DD') === props.currentPageDate : false
    
    // 判断是否是今天
    const isToday = time.format('YYYY-MM-DD') === dayjs().format('YYYY-MM-DD')
    
    // 判断是否是昨天或明天
    const yesterday = dayjs().subtract(1, 'day').format('YYYY-MM-DD')
    const tomorrow = dayjs().add(1, 'day').format('YYYY-MM-DD')
    const isYesterday = time.format('YYYY-MM-DD') === yesterday
    const isTomorrow = time.format('YYYY-MM-DD') === tomorrow
    
    markers.push({
      time: time.format('HH:mm'),
      date: isNewDay ? time.format('MM-DD') : '',
      fullDate: isNewDay ? time.format('YYYY-MM-DD') : '',
      position,
      isMajor,
      isNewDay,
      isCurrentHour: time.isSame(dayjs(), 'hour'),
      isCurrentPage,
      isToday,
      isYesterday,
      isTomorrow
    })
  }
  
  return markers
})

// 当前时间线位置
const currentTimePosition = computed(() => {
  const now = dayjs(getCurrentTime())
  const start = dayjs(props.timelineStart)
  
  if (now.isBefore(start) || now.isAfter(dayjs(props.timelineEnd))) {
    return -1 // 不在显示范围内
  }
  
  const minutes = now.diff(start, 'minute')
  return (minutes / 60) * props.pixelsPerHour
})

// 鼠标滚轮缩放
function handleWheel(event: WheelEvent) {
  if (event.ctrlKey) {
    event.preventDefault()
    
    const delta = event.deltaY > 0 ? 0.8 : 1.2
    const newPixelsPerHour = Math.max(60, Math.min(400, props.pixelsPerHour * delta))
    
    emit('update:pixelsPerHour', newPixelsPerHour)
  } else {
    // 普通滚动 - 直接传递滚动值
    if (timelineRef.value) {
      const newScrollLeft = timelineRef.value.scrollLeft + event.deltaY
      emit('scroll', newScrollLeft)
    }
  }
}

// 鼠标拖拽开始
function handleMouseDown(event: MouseEvent) {
  if (event.button === 0) { // 左键
    isDragging.value = true
    dragStartX.value = event.clientX
    initialScrollLeft.value = props.scrollLeft
    
    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
    event.preventDefault()
  }
}

// 鼠标拖拽移动
function handleMouseMove(event: MouseEvent) {
  if (isDragging.value) {
    const deltaX = event.clientX - dragStartX.value
    const newScrollLeft = initialScrollLeft.value - deltaX
    emit('scroll', newScrollLeft)
  }
}

// 鼠标拖拽结束
function handleMouseUp() {
  isDragging.value = false
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
}

// 点击时间轴
function handleTimelineClick(event: MouseEvent) {
  if (!timelineRef.value) return
  
  const rect = timelineRef.value.getBoundingClientRect()
  const clickX = event.clientX - rect.left + props.scrollLeft
  const minutes = (clickX / props.pixelsPerHour) * 60
  const clickTime = dayjs(props.timelineStart).add(minutes, 'minute')
  
  // 触发时间轴点击事件
  console.log('Timeline clicked at:', clickTime.format('YYYY-MM-DD HH:mm:ss'))
}

// 监听滚动位置变化
watch(() => props.scrollLeft, (newValue) => {
  if (timelineRef.value && !isDragging.value && !isUpdatingScroll) {
    isUpdatingScroll = true
    timelineRef.value.scrollLeft = newValue
    setTimeout(() => {
      isUpdatingScroll = false
    }, 10)
  }
}, { immediate: true })

// 监听时间轴宽度变化，确保滚动同步
watch(() => timelineWidth.value, () => {
  if (timelineRef.value) {
    timelineRef.value.scrollLeft = props.scrollLeft
  }
})

watch(() => props.scrollTop, (newValue) => {
  if (timelineRef.value && !isDragging.value) {
    timelineRef.value.scrollTop = newValue
  }
})

// 处理时间轴自身的滚动事件
function handleTimelineScroll(event: Event) {
  const target = event.target as HTMLElement
  if (!isDragging.value && !isUpdatingScroll) {
    emit('scroll', target.scrollLeft)
  }
}


// 防止滚动事件循环
let isUpdatingScroll = false

onMounted(() => {
  if (timelineRef.value) {
    timelineRef.value.scrollLeft = props.scrollLeft
    timelineRef.value.scrollTop = props.scrollTop || 0
  }
  
  // 定期同步滚动位置
  const syncInterval = setInterval(() => {
    if (timelineRef.value && !isDragging.value && !isUpdatingScroll) {
      if (Math.abs(timelineRef.value.scrollLeft - props.scrollLeft) > 1) {
        timelineRef.value.scrollLeft = props.scrollLeft
      }
    }
  }, 100)
  
  onUnmounted(() => {
    clearInterval(syncInterval)
  })
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
})
</script>

<template>
  <div 
    ref="timelineRef"
    class="timeline-header"
    @wheel="handleWheel"
    @mousedown="handleMouseDown"
    @click="handleTimelineClick"
    @scroll="handleTimelineScroll"
    :style="{ 
      width: timelineWidth + 'px',
      minWidth: '100%',
      transform: `translateX(-${props.scrollLeft}px)`
    }"
  >
    <!-- 时间刻度 -->
    <div class="time-markers">
      <div 
        v-for="marker in timeMarkers"
        :key="marker.time"
        class="time-marker"
        :class="{ 
          'major': marker.isMajor,
          'new-day': marker.isNewDay,
          'current-hour': marker.isCurrentHour,
          'current-page': marker.isCurrentPage,
          'today': marker.isToday,
          'yesterday': marker.isYesterday,
          'tomorrow': marker.isTomorrow
        }"
        :style="{ left: marker.position + 'px' }"
      >
        <div class="time-label">{{ marker.time }}</div>
        <div v-if="marker.date" class="date-label">
          <span v-if="marker.isToday" class="date-tag today-tag">今天</span>
          <span v-else-if="marker.isYesterday" class="date-tag yesterday-tag">昨天</span>
          <span v-else-if="marker.isTomorrow" class="date-tag tomorrow-tag">明天</span>
          <span v-else>{{ marker.date }}</span>
        </div>
      </div>
    </div>

    <!-- 当前时间线 -->
    <div 
      v-if="currentTimePosition >= 0 && props.timelineStart && props.timelineEnd"
      class="current-time-line"
      :style="{ left: currentTimePosition + 'px' }"
    >
      <div class="time-line"></div>
      <div class="time-indicator">
        <div class="time-text">{{ formatTime(getCurrentTime(), 'HH:mm') }}</div>
      </div>
    </div>

    <!-- 时间网格线 -->
    <div class="time-grid">
      <div 
        v-for="marker in timeMarkers"
        :key="'grid-' + marker.time"
        class="grid-line"
        :class="{ 'major': marker.isMajor }"
        :style="{ left: marker.position + 'px' }"
      ></div>
    </div>
  </div>
</template>

<style scoped>
.timeline-header {
  position: relative;
  height: 80px;
  background: var(--timeline-bg);
  border-bottom: 1px solid var(--border-color);
  overflow: hidden;
  cursor: grab;
}

.timeline-header:active {
  cursor: grabbing;
}

.time-markers {
  position: relative;
  height: 100%;
}

.time-marker {
  position: absolute;
  top: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-width: 60px;
}

.time-marker.major {
  font-weight: 600;
}

.time-marker.new-day {
  background: rgba(33, 150, 243, 0.1);
  border-left: 2px solid #2196f3;
  padding-left: 4px;
}

.time-marker.current-hour {
  background: rgba(255, 68, 68, 0.1);
  border-left: 2px solid #ff4444;
  padding-left: 4px;
}

.time-marker.current-page {
  background: rgba(33, 150, 243, 0.2);
  border-left: 3px solid #2196f3;
  padding-left: 4px;
  font-weight: 600;
}

.time-marker.today {
  background: rgba(76, 175, 80, 0.2);
  border-left: 3px solid #4caf50;
  padding-left: 4px;
  font-weight: 600;
}

.time-marker.yesterday {
  background: rgba(255, 152, 0, 0.2);
  border-left: 3px solid #ff9800;
  padding-left: 4px;
  font-weight: 600;
}

.time-marker.tomorrow {
  background: rgba(156, 39, 176, 0.2);
  border-left: 3px solid #9c27b0;
  padding-left: 4px;
  font-weight: 600;
}

.date-tag {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
  font-weight: 600;
  color: white;
}

.today-tag {
  background: #4caf50;
}

.yesterday-tag {
  background: #ff9800;
}

.tomorrow-tag {
  background: #9c27b0;
}

.time-label {
  font-size: 12px;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.date-label {
  font-size: 10px;
  color: var(--text-secondary);
}

.current-time-line {
  position: absolute;
  top: 0;
  bottom: 0;
  z-index: 20;
  pointer-events: none;
}

.time-line {
  width: 2px;
  height: 100%;
  background: #ff4444;
  margin: 0 auto;
}

.time-indicator {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  background: #ff4444;
  color: white;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 10px;
  font-weight: 600;
}

.time-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.grid-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
  background: rgba(0, 0, 0, 0.1);
}

.grid-line.major {
  background: rgba(0, 0, 0, 0.2);
  width: 2px;
}
</style>
