<!-- 甘特图主体区域 -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useGanttStore } from '@/stores/gantt'
import TimelineHeader from './TimelineHeader.vue'
import VehicleList from './VehicleList.vue'
import TrackContainer from './TrackContainer.vue'

const ganttStore = useGanttStore()

// 滚动同步标志
const isScrolling = ref(false)

// 水平滚动位置
const scrollLeft = ref(0)

// 垂直滚动位置  
const scrollTop = ref(0)

// 水平滚动处理
function handleHorizontalScroll(left: number) {
  if (!isScrolling.value) {
    isScrolling.value = true
    scrollLeft.value = left
    // 通知其他组件同步滚动
    setTimeout(() => {
      isScrolling.value = false
    }, 10)
  }
}

// 垂直滚动处理
function handleVerticalScroll(top: number) {
  if (!isScrolling.value) {
    isScrolling.value = true
    scrollTop.value = top
    setTimeout(() => {
      isScrolling.value = false
    }, 10)
  }
}

// 键盘事件处理
function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    // 关闭所有面板
    ganttStore.hideContextMenu()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="gantt-main" :class="{ 'vertical-mode': ganttStore.viewMode === 'vertical' }">
    <!-- 横向模式布局 -->
    <template v-if="ganttStore.viewMode === 'horizontal'">
      <div class="gantt-header">
        <div class="vehicle-header"></div>
        <TimelineHeader 
          :timeline-start="ganttStore.timelineStart"
          :timeline-end="ganttStore.timelineEnd"
          :pixels-per-hour="ganttStore.pixelsPerHour"
          :scroll-left="scrollLeft"
          @scroll="handleHorizontalScroll"
          @update:pixels-per-hour="ganttStore.pixelsPerHour = $event"
        />
      </div>
      
      <div class="gantt-content">
        <VehicleList 
          :vehicles="ganttStore.vehicles"
          :scroll-top="scrollTop"
          @scroll="handleVerticalScroll"
        />
        
        <TrackContainer
          :vehicles="ganttStore.vehicles"
          :timeline-start="ganttStore.timelineStart"
          :timeline-end="ganttStore.timelineEnd"
          :pixels-per-hour="ganttStore.pixelsPerHour"
          :scroll-left="scrollLeft"
          :scroll-top="scrollTop"
          @horizontal-scroll="handleHorizontalScroll"
          @vertical-scroll="handleVerticalScroll"
        />
      </div>
    </template>

    <!-- 纵向模式布局 -->
    <template v-else>
      <div class="gantt-header-vertical">
        <div class="time-header"></div>
        <div class="vehicle-header-vertical">
          <VehicleList 
            :vehicles="ganttStore.vehicles"
            :scroll-left="scrollLeft"
            @scroll="handleHorizontalScroll"
          />
        </div>
      </div>
      
      <div class="gantt-content-vertical">
        <TimelineHeader 
          :timeline-start="ganttStore.timelineStart"
          :timeline-end="ganttStore.timelineEnd"
          :pixels-per-hour="ganttStore.pixelsPerHour"
          :scroll-top="scrollTop"
          @scroll="handleVerticalScroll"
          @update:pixels-per-hour="ganttStore.pixelsPerHour = $event"
        />
        
        <TrackContainer
          :vehicles="ganttStore.vehicles"
          :timeline-start="ganttStore.timelineStart"
          :timeline-end="ganttStore.timelineEnd"
          :pixels-per-hour="ganttStore.pixelsPerHour"
          :scroll-left="scrollLeft"
          :scroll-top="scrollTop"
          view-mode="vertical"
          @horizontal-scroll="handleHorizontalScroll"
          @vertical-scroll="handleVerticalScroll"
        />
      </div>
    </template>
  </div>
</template>

<style scoped>
.gantt-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: white;
}

/* 横向模式布局 */
.gantt-main:not(.vertical-mode) .gantt-header {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  background: var(--timeline-bg);
  z-index: 10;
}

.gantt-main:not(.vertical-mode) .vehicle-header {
  width: 200px;
  border-right: 1px solid var(--border-color);
  background: #f8f9fa;
}

.gantt-main:not(.vertical-mode) .gantt-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* 纵向模式布局 */
.gantt-main.vertical-mode .gantt-header-vertical {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  background: var(--timeline-bg);
  z-index: 10;
}

.gantt-main.vertical-mode .time-header {
  width: 200px;
  border-right: 1px solid var(--border-color);
  background: #f8f9fa;
}

.gantt-main.vertical-mode .vehicle-header-vertical {
  flex: 1;
  overflow: hidden;
}

.gantt-main.vertical-mode .gantt-content-vertical {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.gantt-main.vertical-mode .gantt-content-vertical .timeline-header {
  width: 200px;
  border-right: 1px solid var(--border-color);
}
</style>
