<!-- 行程和任务组件 -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Trip, Vehicle, ViewMode, Task } from '@/types'
import { timeToPx } from '@/utils/time'
import { useTaskTypeStore } from '@/stores/taskType'

interface Props {
  trip: Trip
  vehicle: Vehicle
  timelineStart: string
  timelineEnd: string
  pixelsPerHour: number
  viewMode?: ViewMode
}

const props = withDefaults(defineProps<Props>(), {
  viewMode: 'horizontal'
})

const emit = defineEmits<{
  tripDragStart: [payload: any]
  tripDragEnd: [payload: any]
  resizeStart: [payload: any]
  resizeEnd: [payload: any]
  taskClick: [task: Task]
  taskContextMenu: [event: MouseEvent, task: Task]
}>()

const taskTypeStore = useTaskTypeStore()

// 拖拽状态
const isDragging = ref(false)
const isResizing = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)
const initialPosition = ref({ left: 0, width: 0 })

// 计算属性
const tripStyle = computed(() => {
  const startPx = timeToPx(props.trip.startTime, props.timelineStart, props.pixelsPerHour)
  const endPx = timeToPx(props.trip.endTime, props.timelineStart, props.pixelsPerHour)
  const width = endPx - startPx
  
  return {
    left: startPx + 'px',
    width: Math.max(width, 20) + 'px', // 最小宽度20px
    backgroundColor: props.trip.fullLoad === 'Y' ? '#ffcdd2' : 'var(--trip-background)'
  }
})

const tripHeaderStyle = computed(() => ({
  backgroundColor: props.trip.fullLoad === 'Y' ? '#f44336' : '#2196f3'
}))

const canAddTask = computed(() => {
  return props.trip.fullLoad !== 'Y' && props.trip.tasks.length < 2
})

// 鼠标按下处理
function handleMouseDown(event: MouseEvent) {
  const target = event.target as HTMLElement
  
  // 检查是否点击在调整大小的手柄上
  if (target.classList.contains('resize-handle-left') || target.classList.contains('resize-handle-right')) {
    handleResizeStart(event, target.classList.contains('resize-handle-left') ? 'left' : 'right')
    return
  }
  
  // 检查是否点击在任务上
  if (target.closest('.task-item')) {
    const taskElement = target.closest('.task-item')
    const taskId = taskElement?.getAttribute('data-task-id')
    const task = props.trip.tasks.find(t => t.id === taskId)
    if (task) {
      emit('taskClick', task)
      return
    }
  }
  
  // 开始拖拽行程
  isDragging.value = true
  dragStartX.value = event.clientX
  dragStartY.value = event.clientY
  
  initialPosition.value = {
    left: parseFloat(props.trip.startTime),
    width: parseFloat(props.trip.endTime) - parseFloat(props.trip.startTime)
  }
  
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
  
  emit('tripDragStart', {
    trip: props.trip,
    vehicle: props.vehicle
  })
  
  event.preventDefault()
}

// 鼠标移动处理
function handleMouseMove(event: MouseEvent) {
  if (isDragging.value) {
    const deltaX = event.clientX - dragStartX.value
    const deltaY = event.clientY - dragStartY.value
    
    // 计算新的时间位置
    const minutesPerPixel = 60 / props.pixelsPerHour
    const deltaMinutes = deltaX * minutesPerPixel
    const newStartTime = new Date(new Date(props.trip.startTime).getTime() + deltaMinutes * 60 * 1000)
    
    // 更新行程位置（临时）
    // TODO: 实现实时拖拽预览
    console.log('Dragging trip:', props.trip.id, 'to:', newStartTime)
  } else if (isResizing.value) {
    const deltaX = event.clientX - dragStartX.value
    const minutesPerPixel = 60 / props.pixelsPerHour
    const deltaMinutes = deltaX * minutesPerPixel
    
    // TODO: 实现调整大小逻辑
    console.log('Resizing trip:', props.trip.id, 'delta:', deltaMinutes)
  }
}

// 鼠标释放处理
function handleMouseUp(event: MouseEvent) {
  if (isDragging.value) {
    isDragging.value = false
    
    // 计算最终位置
    const deltaX = event.clientX - dragStartX.value
    const minutesPerPixel = 60 / props.pixelsPerHour
    const deltaMinutes = deltaX * minutesPerPixel
    const newStartTime = new Date(new Date(props.trip.startTime).getTime() + deltaMinutes * 60 * 1000)
    const newEndTime = new Date(new Date(props.trip.endTime).getTime() + deltaMinutes * 60 * 1000)
    
    emit('tripDragEnd', {
      trip: props.trip,
      vehicle: props.vehicle,
      endX: event.clientX,
      endY: event.clientY,
      newStartTime: newStartTime.toISOString().slice(0, 19).replace('T', ' '),
      newEndTime: newEndTime.toISOString().slice(0, 19).replace('T', ' ')
    })
  } else if (isResizing.value) {
    isResizing.value = false
    
    // 计算新的时间范围
    const deltaX = event.clientX - dragStartX.value
    const minutesPerPixel = 60 / props.pixelsPerHour
    const deltaMinutes = deltaX * minutesPerPixel
    
    let newStartTime = new Date(props.trip.startTime)
    let newEndTime = new Date(props.trip.endTime)
    
    // TODO: 根据调整方向更新开始或结束时间
    newEndTime = new Date(newEndTime.getTime() + deltaMinutes * 60 * 1000)
    
    emit('resizeEnd', {
      trip: props.trip,
      vehicle: props.vehicle,
      newStartTime: newStartTime.toISOString().slice(0, 19).replace('T', ' '),
      newEndTime: newEndTime.toISOString().slice(0, 19).replace('T', ' ')
    })
  }
  
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
}

// 开始调整大小
function handleResizeStart(event: MouseEvent, direction: 'left' | 'right') {
  isResizing.value = true
  dragStartX.value = event.clientX
  
  emit('resizeStart', {
    trip: props.trip,
    vehicle: props.vehicle,
    direction
  })
  
  event.preventDefault()
  event.stopPropagation()
}

// 任务点击处理
function handleTaskClick(task: Task) {
  emit('taskClick', task)
}

// 任务右键菜单
function handleTaskContextMenu(event: MouseEvent, task: Task) {
  emit('taskContextMenu', event, task)
}

// 添加任务
function addTask() {
  if (canAddTask.value) {
    // TODO: 打开添加任务面板
    console.log('Add task to trip:', props.trip.id)
  }
}

// 右键菜单
function handleContextMenu(event: MouseEvent) {
  event.preventDefault()
  event.stopPropagation()
  // TODO: 显示右键菜单
  console.log('Trip context menu:', props.trip.id)
}
</script>

<template>
  <div 
    class="trip-container"
    :style="tripStyle"
    @mousedown="handleMouseDown"
    @contextmenu="handleContextMenu"
  >
    <!-- 行程头部 -->
    <div class="trip-header" :style="tripHeaderStyle">
      <div class="trip-info">
        <span class="trip-id">{{ trip.id }}</span>
        <span class="trip-status">{{ trip.fullLoad === 'Y' ? '满载' : '未满载' }}</span>
      </div>
      <div class="trip-actions">
        <button 
          v-if="canAddTask"
          class="add-task-btn"
          @click="addTask"
          title="添加任务"
        >
          +
        </button>
      </div>
    </div>
    
    <!-- 任务列表 -->
    <div class="tasks-container">
      <div
        v-for="task in trip.tasks"
        :key="task.id"
        class="task-item"
        :data-task-id="task.id"
        :style="{ 
          backgroundColor: taskTypeStore.getTaskTypeColor(task.taskType),
          color: 'white'
        }"
        @click="handleTaskClick(task)"
        @contextmenu="handleTaskContextMenu($event, task)"
      >
        <div class="task-info">
          <div class="task-type">{{ task.taskType }}</div>
          <div class="task-address">{{ task.startAddress }}</div>
        </div>
      </div>
    </div>
    
    <!-- 调整大小手柄 -->
    <div class="resize-handle-left" @mousedown="handleResizeStart($event, 'left')"></div>
    <div class="resize-handle-right" @mousedown="handleResizeStart($event, 'right')"></div>
  </div>
</template>

<style scoped>
.trip-container {
  position: absolute;
  top: 0;
  height: 100%;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  cursor: move;
  user-select: none;
  z-index: 10;
}

.trip-container:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.trip-header {
  height: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 8px;
  color: white;
  font-size: 12px;
  font-weight: 600;
}

.trip-info {
  display: flex;
  gap: 8px;
  align-items: center;
}

.trip-status {
  font-size: 10px;
  opacity: 0.9;
}

.add-task-btn {
  width: 16px;
  height: 16px;
  border: none;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 2px;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-task-btn:hover {
  background: rgba(255, 255, 255, 0.5);
}

.tasks-container {
  padding: 4px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.task-item {
  height: 20px;
  border-radius: 2px;
  padding: 2px 6px;
  cursor: pointer;
  font-size: 10px;
  display: flex;
  align-items: center;
  transition: opacity 0.2s;
}

.task-item:hover {
  opacity: 0.8;
}

.task-info {
  overflow: hidden;
  white-space: nowrap;
}

.task-type {
  font-weight: 600;
}

.task-address {
  font-size: 9px;
  opacity: 0.9;
  overflow: hidden;
  text-overflow: ellipsis;
}

.resize-handle-left,
.resize-handle-right {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 4px;
  cursor: ew-resize;
  z-index: 20;
}

.resize-handle-left {
  left: -2px;
}

.resize-handle-right {
  right: -2px;
}

.resize-handle-left:hover,
.resize-handle-right:hover {
  background: rgba(33, 150, 243, 0.3);
}
</style>
