<!-- 甘特图主体区域 -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useGanttStore } from '@/stores/gantt'
import TimelineHeader from './TimelineHeader.vue'
import VehicleList from './VehicleList.vue'
import TrackContainer from './TrackContainer.vue'
import dayjs from 'dayjs'

const ganttStore = useGanttStore()

// 滚动同步标志 - 防止循环触发
const isVerticalScrolling = ref(false)
const isHorizontalScrolling = ref(false)

// 水平滚动位置
const scrollLeft = ref(0)

// 垂直滚动位置  
const scrollTop = ref(0)

// 当前页面日期 - 这是时间轴的核心概念
const currentPageDate = ref(dayjs().format('YYYY-MM-DD'))

// 时间轴偏移量 - 用于连续滚动
const timelineOffset = ref(0) // 以小时为单位

// 计算实际的时间轴范围 - 基于当前页面日期和偏移量
const timelineRange = computed(() => {
  const baseDate = dayjs(currentPageDate.value)
  const offsetHours = timelineOffset.value
  
  return {
    start: baseDate.add(offsetHours, 'hour').startOf('day').format('YYYY-MM-DD HH:mm:ss'),
    end: baseDate.add(offsetHours, 'hour').endOf('day').format('YYYY-MM-DD HH:mm:ss')
  }
})

// 计算车辆列表高度 - 确保与时间轴同步（包括10个空槽位）
const vehicleListHeight = computed(() => {
  const totalSlots = ganttStore.vehicles.length + 10 // 现有车辆 + 10个空槽位
  return totalSlots * 120 // 每辆车120px高度
})

// 水平滚动处理 - 优雅的连续滚动
function handleHorizontalScroll(left: number) {
  if (!isHorizontalScrolling.value) {
    isHorizontalScrolling.value = true
    scrollLeft.value = left
    
    // 计算当前偏移的小时数
    const currentOffsetHours = Math.round(left / ganttStore.pixelsPerHour)
    
    // 检查是否需要切换日期 - 更敏感的切换逻辑
    const hoursPerDay = 24
    const pixelsPerDay = hoursPerDay * ganttStore.pixelsPerHour
    
    // 如果滚动到左边界（查看昨天）
    if (left <= 0) {
      const newDate = dayjs(currentPageDate.value).subtract(1, 'day').format('YYYY-MM-DD')
      currentPageDate.value = newDate
      scrollLeft.value = pixelsPerDay - 100 // 滚动到右边界附近
      console.log('切换到昨天:', newDate)
    }
    // 如果滚动到右边界（查看明天）
    else if (left >= pixelsPerDay - 100) {
      const newDate = dayjs(currentPageDate.value).add(1, 'day').format('YYYY-MM-DD')
      currentPageDate.value = newDate
      scrollLeft.value = 100 // 滚动到左边界附近
      console.log('切换到明天:', newDate)
    }
    // 正常滚动
    else {
      timelineOffset.value = currentOffsetHours
    }
    
    setTimeout(() => {
      isHorizontalScrolling.value = false
    }, 10)
  }
}

// 垂直滚动处理 - 确保左右同步
function handleVerticalScroll(top: number) {
  if (!isVerticalScrolling.value) {
    isVerticalScrolling.value = true
    scrollTop.value = top
    setTimeout(() => {
      isVerticalScrolling.value = false
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

// 监听当前页面日期变化，重置偏移量
watch(currentPageDate, () => {
  timelineOffset.value = 0
  scrollLeft.value = 0
})

// 日期导航函数
function goToPreviousDay() {
  currentPageDate.value = dayjs(currentPageDate.value).subtract(1, 'day').format('YYYY-MM-DD')
  console.log('切换到昨天:', currentPageDate.value)
}

function goToToday() {
  currentPageDate.value = dayjs().format('YYYY-MM-DD')
  console.log('切换到今天:', currentPageDate.value)
}

function goToNextDay() {
  currentPageDate.value = dayjs(currentPageDate.value).add(1, 'day').format('YYYY-MM-DD')
  console.log('切换到明天:', currentPageDate.value)
}

// 处理新车辆创建
function handleVehicleCreated() {
  // 刷新车辆列表
  ganttStore.fetchVehicleList()
}

// 处理车辆删除
function handleVehicleDeleted() {
  // 刷新车辆列表
  ganttStore.fetchVehicleList()
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  // 初始化时间轴范围
  ganttStore.timelineStart = timelineRange.value.start
  ganttStore.timelineEnd = timelineRange.value.end
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="gantt-main">
    <!-- 全屏横向布局：左边车辆列表，右边时间轴 -->
    <div class="gantt-layout">
      <!-- 左侧车辆列表区域 -->
      <div class="vehicle-panel">
        <div class="vehicle-header">
          <h3 class="panel-title">车辆列表</h3>
          <div class="current-date">
            <span class="date-display">{{ currentPageDate }}</span>
            <div class="date-navigation">
              <button @click="goToPreviousDay" class="nav-btn prev-btn">←</button>
              <button @click="goToToday" class="nav-btn today-btn">今天</button>
              <button @click="goToNextDay" class="nav-btn next-btn">→</button>
            </div>
          </div>
        </div>
        <VehicleList 
          :vehicles="ganttStore.vehicles"
          :scroll-top="scrollTop"
          :height="vehicleListHeight"
          @scroll="handleVerticalScroll"
          @vehicle-created="handleVehicleCreated"
          @vehicle-deleted="handleVehicleDeleted"
        />
      </div>
      
      <!-- 右侧时间轴区域 -->
      <div class="timeline-panel">
        <!-- 时间轴头部 -->
        <div class="timeline-header-container">
          <TimelineHeader 
            :timeline-start="timelineRange.start"
            :timeline-end="timelineRange.end"
            :pixels-per-hour="ganttStore.pixelsPerHour"
            :scroll-left="scrollLeft"
            :current-page-date="currentPageDate"
            @scroll="handleHorizontalScroll"
            @update:pixels-per-hour="ganttStore.pixelsPerHour = $event"
          />
        </div>
        
        <!-- 时间轴内容区域 -->
        <div class="timeline-content">
          <TrackContainer
            :vehicles="ganttStore.vehicles"
            :timeline-start="timelineRange.start"
            :timeline-end="timelineRange.end"
            :pixels-per-hour="ganttStore.pixelsPerHour"
            :scroll-left="scrollLeft"
            :scroll-top="scrollTop"
            :view-mode="ganttStore.viewMode"
            :height="vehicleListHeight"
            @horizontal-scroll="handleHorizontalScroll"
            @vertical-scroll="handleVerticalScroll"
          />
        </div>
      </div>
    </div>
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

.gantt-layout {
  display: flex;
  height: 100%;
  overflow: hidden;
}

/* 左侧车辆面板 */
.vehicle-panel {
  width: 300px;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  border-right: 2px solid var(--border-color);
  background: #f8f9fa;
}

.vehicle-header {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.panel-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.current-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.date-display {
  font-size: 14px;
  color: var(--text-primary);
  background: #e3f2fd;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
}

.date-navigation {
  display: flex;
  gap: 2px;
}

.nav-btn {
  padding: 2px 6px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 3px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.nav-btn:hover {
  background: #f5f5f5;
  border-color: #2196f3;
}

.today-btn {
  background: #2196f3;
  color: white;
  border-color: #2196f3;
}

.today-btn:hover {
  background: #1976d2;
}

/* 右侧时间轴面板 */
.timeline-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.timeline-header-container {
  border-bottom: 1px solid var(--border-color);
  background: var(--timeline-bg);
  z-index: 10;
  flex-shrink: 0;
}

.timeline-content {
  flex: 1;
  overflow: hidden;
  background: white;
}
</style>
