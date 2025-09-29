<!-- 轨道组件 -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Vehicle, ViewMode } from '@/types'
import { useGanttStore } from '@/stores/gantt'
import TripWithTasks from './TripWithTasks.vue'

const ganttStore = useGanttStore()

interface Props {
  vehicle: Vehicle
  timelineStart: string
  timelineEnd: string
  pixelsPerHour: number
  viewMode?: ViewMode
  scrollLeft?: number
  scrollTop?: number
}

const props = withDefaults(defineProps<Props>(), {
  viewMode: 'horizontal',
  scrollLeft: 0,
  scrollTop: 0
})

const emit = defineEmits<{
  tripDragStart: [payload: any]
  tripDragEnd: [payload: any]
  tripResizeStart: [payload: any]
  tripResizeEnd: [payload: any]
  contextMenu: [event: MouseEvent, payload: any]
}>()

// 处理行程拖拽结束
function handleTripDragEnd(payload: any) {
  if (payload.newStartTime && payload.newEndTime) {
    // 调用API更新行程时间
    ganttStore.dragChangeTripTime({
      tripId: payload.trip.id,
      newStart: payload.newStartTime,
      newEnd: payload.newEndTime
    }).catch(error => {
      console.error('Failed to update trip time:', error)
    })
  }
}

// 处理行程调整大小结束
function handleTripResizeEnd(payload: any) {
  if (payload.newStartTime && payload.newEndTime) {
    // 调用API更新行程时间
    ganttStore.dragChangeTripTime({
      tripId: payload.trip.id,
      newStart: payload.newStartTime,
      newEnd: payload.newEndTime
    }).catch(error => {
      console.error('Failed to resize trip:', error)
    })
  }
}

// 轨道引用
const trackRef = ref<HTMLElement>()

// 计算属性
const trackStyle = computed(() => ({
  height: props.viewMode === 'horizontal' ? 'var(--row-height)' : 'auto',
  width: props.viewMode === 'vertical' ? 'var(--row-height)' : 'auto',
  minHeight: props.viewMode === 'horizontal' ? 'var(--row-height)' : 'auto',
  minWidth: props.viewMode === 'vertical' ? 'var(--row-height)' : 'auto'
}))

// 右键菜单处理
function handleContextMenu(event: MouseEvent) {
  event.preventDefault()
  emit('contextMenu', event, { vehicle: props.vehicle, type: 'track' })
}

// 空白区域点击
function handleTrackClick(event: MouseEvent) {
  if (event.target === trackRef.value) {
    // 空白区域点击，用于创建新行程
    console.log('Track clicked:', props.vehicle.id)
  }
}
</script>

<template>
  <div 
    ref="trackRef"
    class="track"
    :class="{ 'vertical': viewMode === 'vertical' }"
    :data-vehicle-id="vehicle.id"
    :style="trackStyle"
    @contextmenu="handleContextMenu"
    @click="handleTrackClick"
  >
    <!-- 行程和任务 -->
    <TripWithTasks
      v-for="trip in vehicle.trips"
      :key="trip.id"
      :trip="trip"
      :vehicle="vehicle"
      :timeline-start="timelineStart"
      :timeline-end="timelineEnd"
      :pixels-per-hour="pixelsPerHour"
      :view-mode="viewMode"
      @trip-drag-start="emit('tripDragStart', $event)"
      @trip-drag-end="handleTripDragEnd"
      @resize-start="emit('tripResizeStart', $event)"
      @resize-end="handleTripResizeEnd"
    />
  </div>
</template>

<style scoped>
.track {
  position: relative;
  border-bottom: 1px solid var(--border-color);
  background: white;
  cursor: pointer;
}

.track:hover {
  background: #f8f9fa;
}

.track.vertical {
  border-bottom: none;
  border-right: 1px solid var(--border-color);
}

.track.vertical:hover {
  background: #f8f9fa;
}
</style>
