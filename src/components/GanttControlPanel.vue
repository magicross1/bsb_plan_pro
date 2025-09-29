<!-- 甘特图控制面板 -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import { 
  ElButton, 
  ElButtonGroup, 
  ElSelect, 
  ElOption, 
  ElDatePicker,
  ElTooltip,
  ElIcon
} from 'element-plus'
import { 
  Refresh, 
  Plus, 
  Setting, 
  Switch, 
  ZoomIn, 
  ZoomOut,
  Calendar,
  Van
} from '@element-plus/icons-vue'
import { useGanttStore } from '@/stores/gantt'
import { useOrderSelectionStore } from '@/stores/orderSelection'
import { getCurrentTime } from '@/utils/time'

const ganttStore = useGanttStore()
const orderSelectionStore = useOrderSelectionStore()

// 时间范围快捷选项
const timeRangeOptions = [
  { label: '今天', value: 'today' },
  { label: '明天', value: 'tomorrow' },
  { label: '本周', value: 'week' },
  { label: '自定义', value: 'custom' }
]

const selectedTimeRange = ref('today')

// 缩放选项
const zoomOptions = [
  { label: '0.5x', value: 60 },
  { label: '1x', value: 100 },
  { label: '2x', value: 200 },
  { label: '4x', value: 400 }
]

// 设置面板可见性
const settingsVisible = ref(false)

// 时间范围处理
function handleTimeRangeChange(range: string) {
  selectedTimeRange.value = range
  
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  
  switch (range) {
    case 'today':
      ganttStore.timelineStart = today.toISOString().slice(0, 19).replace('T', ' ')
      ganttStore.timelineEnd = new Date(today.getTime() + 24 * 60 * 60 * 1000).toISOString().slice(0, 19).replace('T', ' ')
      break
    case 'tomorrow':
      const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000)
      ganttStore.timelineStart = tomorrow.toISOString().slice(0, 19).replace('T', ' ')
      ganttStore.timelineEnd = new Date(tomorrow.getTime() + 24 * 60 * 60 * 1000).toISOString().slice(0, 19).replace('T', ' ')
      break
    case 'week':
      const weekStart = new Date(today)
      weekStart.setDate(today.getDate() - today.getDay())
      const weekEnd = new Date(weekStart.getTime() + 7 * 24 * 60 * 60 * 1000)
      ganttStore.timelineStart = weekStart.toISOString().slice(0, 19).replace('T', ' ')
      ganttStore.timelineEnd = weekEnd.toISOString().slice(0, 19).replace('T', ' ')
      break
  }
  
  // 刷新数据
  ganttStore.fetchVehicleList()
}

// 缩放处理
function handleZoomChange(value: number) {
  ganttStore.pixelsPerHour = value
}

// 放大
function zoomIn() {
  const current = ganttStore.pixelsPerHour
  const next = zoomOptions.find(opt => opt.value > current)
  if (next) {
    ganttStore.pixelsPerHour = next.value
  }
}

// 缩小
function zoomOut() {
  const current = ganttStore.pixelsPerHour
  const prev = [...zoomOptions].reverse().find(opt => opt.value < current)
  if (prev) {
    ganttStore.pixelsPerHour = prev.value
  }
}

// 刷新数据
function refreshData() {
  ganttStore.fetchVehicleList()
}

// 新增行程
function addTrip() {
  // TODO: 打开新增行程面板
  console.log('Add new trip')
}

// 打开订单面板
function openOrders() {
  orderSelectionStore.show()
}

// 打开设置
function openSettings() {
  settingsVisible.value = true
}

// 切换视图模式
function toggleViewMode() {
  ganttStore.toggleViewMode()
}

// 自定义时间范围
const customTimeRange = ref<[Date, Date] | null>(null)

function handleCustomTimeRange(dates: [Date, Date] | null) {
  if (dates && dates.length === 2) {
    ganttStore.timelineStart = dates[0].toISOString().slice(0, 19).replace('T', ' ')
    ganttStore.timelineEnd = dates[1].toISOString().slice(0, 19).replace('T', ' ')
    ganttStore.fetchVehicleList()
  }
}
</script>

<template>
  <div class="control-panel">
    <div class="control-left">
      <!-- 时间范围选择 -->
      <ElSelect 
        v-model="selectedTimeRange" 
        @change="handleTimeRangeChange"
        placeholder="时间范围"
        style="width: 120px"
      >
        <ElOption
          v-for="option in timeRangeOptions"
          :key="option.value"
          :label="option.label"
          :value="option.value"
        />
      </ElSelect>

      <!-- 自定义时间范围 -->
      <ElDatePicker
        v-if="selectedTimeRange === 'custom'"
        v-model="customTimeRange"
        type="datetimerange"
        range-separator="至"
        start-placeholder="开始时间"
        end-placeholder="结束时间"
        format="YYYY-MM-DD HH:mm:ss"
        value-format="YYYY-MM-DD HH:mm:ss"
        @change="handleCustomTimeRange"
        style="width: 320px"
      />

      <!-- 缩放控制 -->
      <ElSelect 
        :model-value="ganttStore.pixelsPerHour"
        @change="handleZoomChange"
        placeholder="缩放"
        style="width: 80px"
      >
        <ElOption
          v-for="option in zoomOptions"
          :key="option.value"
          :label="option.label"
          :value="option.value"
        />
      </ElSelect>

      <ElButtonGroup>
        <ElButton @click="zoomOut" :disabled="ganttStore.pixelsPerHour <= 60">
          <ElIcon><ZoomOut /></ElIcon>
        </ElButton>
        <ElButton @click="zoomIn" :disabled="ganttStore.pixelsPerHour >= 400">
          <ElIcon><ZoomIn /></ElIcon>
        </ElButton>
      </ElButtonGroup>
    </div>

    <div class="control-center">
      <!-- 当前时间显示 -->
      <div class="current-time">
        <ElIcon><Calendar /></ElIcon>
        <span>{{ getCurrentTime() }}</span>
      </div>
    </div>

    <div class="control-right">
      <!-- 操作按钮 -->
      <ElButtonGroup>
        <ElTooltip content="刷新数据" placement="bottom">
          <ElButton @click="refreshData">
            <ElIcon><Refresh /></ElIcon>
          </ElButton>
        </ElTooltip>
        
        <ElTooltip content="新增行程" placement="bottom">
          <ElButton @click="addTrip">
            <ElIcon><Plus /></ElIcon>
          </ElButton>
        </ElTooltip>
        
        <ElTooltip content="打开订单" placement="bottom">
          <ElButton @click="openOrders">
            <ElIcon><Van /></ElIcon>
          </ElButton>
        </ElTooltip>
        
        <ElTooltip content="设置" placement="bottom">
          <ElButton @click="openSettings">
            <ElIcon><Setting /></ElIcon>
          </ElButton>
        </ElTooltip>
      </ElButtonGroup>

      <!-- 模式切换 -->
      <ElButton 
        @click="toggleViewMode"
        :type="ganttStore.viewMode === 'vertical' ? 'primary' : ''"
        style="margin-left: 8px"
      >
        <ElIcon><Switch /></ElIcon>
        {{ ganttStore.viewMode === 'horizontal' ? '横' : '纵' }}向
      </ElButton>
    </div>
  </div>
</template>

<style scoped>
.control-panel {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid var(--border-color);
  gap: 16px;
}

.control-left,
.control-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.current-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--text-secondary);
  background: #f5f5f5;
  padding: 6px 12px;
  border-radius: 4px;
}

.control-panel .el-select {
  margin-right: 8px;
}

.control-panel .el-button-group {
  margin-right: 8px;
}
</style>
