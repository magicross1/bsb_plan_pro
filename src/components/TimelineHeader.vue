<!-- 时间轴头部组件 -->
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { formatTime, getCurrentTime, diffMinutes } from '@/utils/time'
import dayjs from 'dayjs'

interface Props {
  timelineStart: string
  timelineEnd: string
  pixelsPerHour: number
  scrollLeft?: number
  scrollTop?: number
}

const props = withDefaults(defineProps<Props>(), {
  scrollLeft: 0,
  scrollTop: 0
})

const emit = defineEmits<{
  scroll: [value: number]
  'update:pixelsPerHour': [value: number]
  rangeChange: [range: { start: string; end: string }]
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

const hoursInRange = computed(() => {
  const start = dayjs(props.timelineStart)
  const end = dayjs(props.timelineEnd)
  return end.diff(start, 'hour')
})

// 时间刻度
const timeMarkers = computed(() => {
  const markers = []
  const start = dayjs(props.timelineStart)
  const end = dayjs(props.timelineEnd)
  const hours = Math.ceil(end.diff(start, 'hour'))
  
  for (let i = 0; i <= hours; i++) {
    const time = start.add(i, 'hour')
    const position = (i * props.pixelsPerHour)
    markers.push({
      time: time.format('HH:mm'),
      date: i % 24 === 0 ? time.format('MM-DD') : '',
      position,
      isMajor: i % 4 === 0 || i === 0
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
    // 普通滚动
    const scrollValue = event.deltaY > 0 ? 100 : -100
    emit('scroll', scrollValue)
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
  
  // TODO: 触发时间轴点击事件
  console.log('Timeline clicked at:', clickTime.format('YYYY-MM-DD HH:mm:ss'))
}

// 监听滚动位置变化
watch(() => props.scrollLeft, (newValue) => {
  if (timelineRef.value && !isDragging.value) {
    timelineRef.value.scrollLeft = newValue
  }
})

watch(() => props.scrollTop, (newValue) => {
  if (timelineRef.value && !isDragging.value) {
    timelineRef.value.scrollTop = newValue
  }
})

onMounted(() => {
  if (timelineRef.value) {
    timelineRef.value.scrollLeft = props.scrollLeft
    timelineRef.value.scrollTop = props.scrollTop || 0
  }
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
    :style="{ 
      width: timelineWidth + 'px',
      minWidth: '100%'
    }"
  >
    <!-- 时间刻度 -->
    <div class="time-markers">
      <div 
        v-for="marker in timeMarkers"
        :key="marker.time"
        class="time-marker"
        :class="{ 'major': marker.isMajor }"
        :style="{ left: marker.position + 'px' }"
      >
        <div class="time-label">{{ marker.time }}</div>
        <div v-if="marker.date" class="date-label">{{ marker.date }}</div>
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
