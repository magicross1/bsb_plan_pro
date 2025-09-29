<!-- 轨道容器组件 -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Vehicle, ViewMode } from '@/types'
import Track from './Track.vue'

interface Props {
  vehicles: Vehicle[]
  timelineStart: string
  timelineEnd: string
  pixelsPerHour: number
  scrollLeft?: number
  scrollTop?: number
  viewMode?: ViewMode
}

const props = withDefaults(defineProps<Props>(), {
  scrollLeft: 0,
  scrollTop: 0,
  viewMode: 'horizontal'
})

const emit = defineEmits<{
  horizontalScroll: [value: number]
  verticalScroll: [value: number]
}>()

// 容器引用
const containerRef = ref<HTMLElement>()

// 计算属性
const timelineWidth = computed(() => {
  const start = new Date(props.timelineStart)
  const end = new Date(props.timelineEnd)
  const diffMinutes = (end.getTime() - start.getTime()) / (1000 * 60)
  return (diffMinutes / 60) * props.pixelsPerHour
})

// 滚动处理
function handleScroll(event: Event) {
  const target = event.target as HTMLElement
  emit('horizontalScroll', target.scrollLeft)
  emit('verticalScroll', target.scrollTop)
}

// 右键菜单处理
function handleContextMenu(event: MouseEvent) {
  event.preventDefault()
  
  const rect = containerRef.value?.getBoundingClientRect()
  if (!rect) return
  
  const x = event.clientX - rect.left + props.scrollLeft
  const y = event.clientY - rect.top + props.scrollTop
  
  // TODO: 显示上下文菜单
  console.log('Context menu at:', x, y)
}

// 框选处理
function handleSelection(event: MouseEvent) {
  // TODO: 实现框选功能
  console.log('Selection:', event)
}
</script>

<template>
  <div 
    ref="containerRef"
    class="track-container"
    @scroll="handleScroll"
    @contextmenu="handleContextMenu"
    @mousedown="handleSelection"
  >
    <div 
      class="tracks-wrapper"
      :style="{ 
        width: timelineWidth + 'px',
        minWidth: '100%'
      }"
    >
      <Track
        v-for="vehicle in vehicles"
        :key="vehicle.id"
        :vehicle="vehicle"
        :timeline-start="timelineStart"
        :timeline-end="timelineEnd"
        :pixels-per-hour="pixelsPerHour"
        :view-mode="viewMode"
        :scroll-left="scrollLeft"
        :scroll-top="scrollTop"
      />
    </div>
  </div>
</template>

<style scoped>
.track-container {
  flex: 1;
  overflow: auto;
  background: white;
  position: relative;
}

.tracks-wrapper {
  position: relative;
  min-height: 100%;
}

/* 时间网格背景 */
.track-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    repeating-linear-gradient(
      to right,
      transparent 0,
      transparent calc(var(--pixels-per-hour, 100px) - 1px),
      rgba(0, 0, 0, 0.05) calc(var(--pixels-per-hour, 100px) - 1px),
      rgba(0, 0, 0, 0.05) var(--pixels-per-hour, 100px)
    );
  pointer-events: none;
  z-index: 1;
}

/* 当前时间线 */
.track-container::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #ff4444;
  z-index: 10;
  pointer-events: none;
}
</style>
