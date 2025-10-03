<!-- 车辆列表组件 -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Vehicle } from '@/types'
import VehicleSelectionDialog from './VehicleSelectionDialog.vue'

interface Props {
  vehicles: Vehicle[]
  scrollTop?: number
  scrollLeft?: number
  height?: number
}

const props = withDefaults(defineProps<Props>(), {
  scrollTop: 0,
  scrollLeft: 0
})

const emit = defineEmits<{
  scroll: [value: number]
  vehicleSelected: [vehicle: Vehicle]
  slotClicked: [slotIndex: number]
  vehicleCreated: [vehicle: Vehicle]
  vehicleDeleted: [vehicleId: string]
}>()

// 选中的车辆
const selectedVehicleId = ref<string | null>(null)

// 空槽位数量
const EMPTY_SLOTS_COUNT = 10

// 可用的车辆和司机选项
const availableVehicles = ref<string[]>([])
const availableDrivers = ref<string[]>([])

// 对话框状态
const showSelectionDialog = ref(false)
const selectedSlotIndex = ref<number>(-1)
const editingVehicle = ref<Vehicle | null>(null)

// 计算属性 - 合并现有车辆和空槽位
const vehicleStats = computed(() => {
  const existingVehicles = props.vehicles.map(vehicle => {
    const totalTrips = vehicle.trips.length
    const totalTasks = vehicle.trips.reduce((sum, trip) => sum + trip.tasks.length, 0)
    const fullLoadTrips = vehicle.trips.filter(trip => trip.fullLoad === 'Y').length
    
    return {
      ...vehicle,
      stats: {
        totalTrips,
        totalTasks,
        fullLoadTrips,
        availableSlots: totalTrips * 2 - totalTasks
      },
      isEmpty: false,
      slotIndex: -1
    }
  })

  // 添加空槽位
  const emptySlots = Array.from({ length: EMPTY_SLOTS_COUNT }, (_, index) => ({
    id: `empty-slot-${index}`,
    plateNumber: '',
    driverId: '',
    trips: [],
    stats: {
      totalTrips: 0,
      totalTasks: 0,
      fullLoadTrips: 0,
      availableSlots: 0
    },
    isEmpty: true,
    slotIndex: index
  }))

  return [...existingVehicles, ...emptySlots]
})

// 获取可用的车辆和司机列表
async function fetchAvailableOptions() {
  try {
    const response = await fetch('/api/gantt/get_vehicle_driver_list')
    const result = await response.json()
    
    if (result.code === 0) {
      availableVehicles.value = result.data[0] || []
      availableDrivers.value = result.data[1] || []
    }
  } catch (error) {
    console.error('Error fetching available options:', error)
  }
}

// 选择车辆
function selectVehicle(vehicle: Vehicle) {
  selectedVehicleId.value = vehicle.id
  emit('vehicleSelected', vehicle)
}

// 点击空槽位
function clickEmptySlot(slotIndex: number) {
  selectedSlotIndex.value = slotIndex
  editingVehicle.value = null
  showSelectionDialog.value = true
}

// 确认车辆选择
async function confirmVehicleSelection(vehicle: string, driver: string) {
  try {
    if (editingVehicle.value) {
      // 编辑现有车辆
      const response = await fetch(`/api/gantt/vehicle/${editingVehicle.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plateNumber: vehicle,
          driverId: driver
        })
      })
      
      const result = await response.json()
      
      if (result.code === 0) {
        // 编辑成功，通知父组件刷新
        emit('vehicleCreated', result.data)
        showSelectionDialog.value = false
      } else {
        console.error('编辑车辆失败:', result.message)
        alert('编辑车辆失败: ' + result.message)
      }
    } else {
      // 创建新车辆
      const response = await fetch('/api/gantt/create_vehicle', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plateNumber: vehicle,
          driverId: driver
        })
      })
      
      const result = await response.json()
      
      if (result.code === 0) {
        // 创建成功，通知父组件
        emit('vehicleCreated', result.data)
        showSelectionDialog.value = false
      } else {
        console.error('创建车辆失败:', result.message)
        alert('创建车辆失败: ' + result.message)
      }
    }
  } catch (error) {
    console.error('操作车辆错误:', error)
    alert('操作车辆时发生错误')
  }
}

// 关闭对话框
function closeSelectionDialog() {
  showSelectionDialog.value = false
  selectedSlotIndex.value = -1
  editingVehicle.value = null
}

// 编辑车辆
function editVehicle(vehicle: Vehicle) {
  // 将车辆信息填入对话框
  editingVehicle.value = vehicle
  showSelectionDialog.value = true
}

// 删除车辆
async function deleteVehicle(vehicle: Vehicle) {
  if (!confirm(`确定要删除车辆 ${vehicle.plateNumber} - ${vehicle.driverId} 吗？`)) {
    return
  }
  
  try {
    const response = await fetch(`/api/gantt/vehicle/${vehicle.id}`, {
      method: 'DELETE'
    })
    
    const result = await response.json()
    
    if (result.code === 0) {
      // 删除成功，通知父组件
      emit('vehicleDeleted', vehicle.id)
    } else {
      console.error('删除车辆失败:', result.message)
      alert('删除车辆失败: ' + result.message)
    }
  } catch (error) {
    console.error('删除车辆错误:', error)
    alert('删除车辆时发生错误')
  }
}

// 滚动处理
function handleScroll(event: Event) {
  const target = event.target as HTMLElement
  emit('scroll', target.scrollTop)
}

onMounted(() => {
  fetchAvailableOptions()
})
</script>

<template>
  <div 
    class="vehicle-list" 
    :style="{ scrollTop: scrollTop + 'px' } as any"
    @scroll="handleScroll"
  >
    <div class="vehicle-list-content">
      <div 
        v-for="vehicle in vehicleStats" 
        :key="vehicle.id"
        class="vehicle-item"
        :class="{ 
          'selected': selectedVehicleId === vehicle.id,
          'empty-slot': vehicle.isEmpty 
        }"
        @click="vehicle.isEmpty ? clickEmptySlot(vehicle.slotIndex) : selectVehicle(vehicle)"
      >
        <!-- 现有车辆显示 -->
        <template v-if="!vehicle.isEmpty">
          <div class="vehicle-header">
            <div class="vehicle-info">{{ vehicle.plateNumber }} - {{ vehicle.driverId }}</div>
            <div class="vehicle-actions">
              <button class="edit-btn" @click.stop="editVehicle(vehicle)" title="编辑">✏️</button>
              <button class="delete-btn" @click.stop="deleteVehicle(vehicle)" title="删除">🗑️</button>
            </div>
          </div>
          
          <div class="vehicle-stats">
            <div class="stat-item">
              <span class="stat-label">行程:</span>
              <span class="stat-value">{{ vehicle.stats.totalTrips }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">任务:</span>
              <span class="stat-value">{{ vehicle.stats.totalTasks }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">满载:</span>
              <span class="stat-value">{{ vehicle.stats.fullLoadTrips }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">余位:</span>
              <span class="stat-value" :class="{ 'warning': vehicle.stats.availableSlots <= 1 }">
                {{ vehicle.stats.availableSlots }}
              </span>
            </div>
          </div>
          
          <div v-if="vehicle.driverId" class="driver-info">
            <span class="driver-label">司机:</span>
            <span class="driver-name">{{ vehicle.driverId }}</span>
          </div>
        </template>

        <!-- 空槽位显示 -->
        <template v-else>
          <div class="empty-slot-content">
            <div class="empty-slot-icon">+</div>
            <div class="empty-slot-text">点击选择车辆和司机</div>
          </div>
        </template>
      </div>
    </div>

    <!-- 车辆选择对话框 -->
    <VehicleSelectionDialog
      :visible="showSelectionDialog"
      :available-vehicles="availableVehicles"
      :available-drivers="availableDrivers"
      :editing-vehicle="editingVehicle"
      @close="closeSelectionDialog"
      @confirm="confirmVehicleSelection"
    />
  </div>
</template>

<style scoped>
.vehicle-list {
  flex: 1;
  background: #f8f9fa;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
}

.vehicle-list::-webkit-scrollbar {
  width: 8px;
}

.vehicle-list::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.vehicle-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.vehicle-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.vehicle-list-content {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.vehicle-item {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: background-color 0.2s;
  height: var(--row-height);
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: white;
  box-sizing: border-box;
}

.vehicle-item:hover {
  background: #e9ecef;
}

.vehicle-item.selected {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.vehicle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.vehicle-info {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.vehicle-actions {
  display: flex;
  gap: 4px;
}

.edit-btn,
.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
  font-size: 12px;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.edit-btn:hover,
.delete-btn:hover {
  opacity: 1;
}

.delete-btn:hover {
  color: #dc3545;
}

.vehicle-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  margin-bottom: 8px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
}

.stat-label {
  color: var(--text-secondary);
}

.stat-value {
  font-weight: 600;
  color: var(--text-primary);
}

.stat-value.warning {
  color: #ff9800;
}

.driver-info {
  font-size: 11px;
  color: var(--text-secondary);
}

.driver-label {
  margin-right: 4px;
}

.driver-name {
  font-weight: 500;
}

/* 空槽位样式 */
.vehicle-item.empty-slot {
  background: #f8f9fa;
  border-left: 4px dashed #dee2e6;
  cursor: pointer;
}

.vehicle-item.empty-slot:hover {
  background: #e9ecef;
  border-left-color: #adb5bd;
}

.empty-slot-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6c757d;
}

.empty-slot-icon {
  font-size: 24px;
  font-weight: 300;
  margin-bottom: 8px;
  opacity: 0.7;
}

.empty-slot-text {
  font-size: 12px;
  text-align: center;
  opacity: 0.8;
}
</style>
