<!-- 车辆列表组件 -->
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Vehicle } from '@/types'

interface Props {
  vehicles: Vehicle[]
  scrollTop?: number
  scrollLeft?: number
}

const props = withDefaults(defineProps<Props>(), {
  scrollTop: 0,
  scrollLeft: 0
})

const emit = defineEmits<{
  scroll: [value: number]
}>()

// 选中的车辆
const selectedVehicleId = ref<string | null>(null)

// 计算属性
const vehicleStats = computed(() => {
  return props.vehicles.map(vehicle => {
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
      }
    }
  })
})

// 选择车辆
function selectVehicle(vehicle: Vehicle) {
  selectedVehicleId.value = vehicle.id
  // TODO: 触发车辆选择事件
  console.log('Selected vehicle:', vehicle)
}

// 滚动处理
function handleScroll(event: Event) {
  const target = event.target as HTMLElement
  emit('scroll', target.scrollTop)
}
</script>

<template>
  <div class="vehicle-list" @scroll="handleScroll">
    <div class="vehicle-list-content">
      <div 
        v-for="vehicle in vehicleStats" 
        :key="vehicle.id"
        class="vehicle-item"
        :class="{ 'selected': selectedVehicleId === vehicle.id }"
        @click="selectVehicle(vehicle)"
      >
        <div class="vehicle-header">
          <div class="vehicle-id">{{ vehicle.id }}</div>
          <div class="plate-number">{{ vehicle.plateNumber }}</div>
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
      </div>
    </div>
  </div>
</template>

<style scoped>
.vehicle-list {
  width: 200px;
  background: #f8f9fa;
  border-right: 1px solid var(--border-color);
  overflow-y: auto;
  overflow-x: hidden;
}

.vehicle-list-content {
  min-height: 100%;
}

.vehicle-item {
  padding: 12px;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: background-color 0.2s;
  min-height: var(--row-height);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.vehicle-item:hover {
  background: #e9ecef;
}

.vehicle-item.selected {
  background: #e3f2fd;
  border-right: 3px solid #2196f3;
}

.vehicle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.vehicle-id {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.plate-number {
  font-size: 12px;
  color: var(--text-secondary);
  background: #e9ecef;
  padding: 2px 6px;
  border-radius: 3px;
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
</style>
