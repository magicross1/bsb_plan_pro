<!-- 车辆选择对话框 -->
<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Vehicle } from '@/types'

interface Props {
  visible: boolean
  availableVehicles: string[]
  availableDrivers: string[]
  editingVehicle?: Vehicle | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
  confirm: [vehicle: string, driver: string]
}>()

// 选中的车辆和司机
const selectedVehicle = ref<string>('')
const selectedDriver = ref<string>('')

// 监听对话框显示状态，重置选择
watch(() => props.visible, (visible) => {
  if (visible) {
    if (props.editingVehicle) {
      selectedVehicle.value = props.editingVehicle.plateNumber
      selectedDriver.value = props.editingVehicle.driverId || ''
    } else {
      selectedVehicle.value = ''
      selectedDriver.value = ''
    }
  }
})

// 确认选择
function confirmSelection() {
  if (selectedVehicle.value && selectedDriver.value) {
    emit('confirm', selectedVehicle.value, selectedDriver.value)
    emit('close')
  }
}

// 取消选择
function cancelSelection() {
  emit('close')
}
</script>

<template>
  <div v-if="visible" class="dialog-overlay" @click="cancelSelection">
    <div class="dialog-content" @click.stop>
      <div class="dialog-header">
        <h3>{{ editingVehicle ? '编辑车辆和司机' : '选择车辆和司机' }}</h3>
        <button class="close-btn" @click="cancelSelection">×</button>
      </div>
      
      <div class="dialog-body">
        <div class="form-group">
          <label for="vehicle-select">车辆:</label>
          <select 
            id="vehicle-select" 
            v-model="selectedVehicle"
            class="form-select"
          >
            <option value="">请选择车辆</option>
            <option 
              v-for="vehicle in availableVehicles" 
              :key="vehicle" 
              :value="vehicle"
            >
              {{ vehicle }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="driver-select">司机:</label>
          <select 
            id="driver-select" 
            v-model="selectedDriver"
            class="form-select"
          >
            <option value="">请选择司机</option>
            <option 
              v-for="driver in availableDrivers" 
              :key="driver" 
              :value="driver"
            >
              {{ driver }}
            </option>
          </select>
        </div>
      </div>
      
      <div class="dialog-footer">
        <button class="btn btn-secondary" @click="cancelSelection">
          取消
        </button>
        <button 
          class="btn btn-primary" 
          @click="confirmSelection"
          :disabled="!selectedVehicle || !selectedDriver"
        >
          {{ editingVehicle ? '保存' : '确认' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 400px;
  max-width: 90vw;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e9ecef;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #212529;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #495057;
}

.dialog-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #495057;
}

.form-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  background: white;
}

.form-select:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e9ecef;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
}
</style>
