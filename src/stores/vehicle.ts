// 车辆基础数据管理

import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Vehicle } from '@/types';

export const useVehicleStore = defineStore('vehicle', () => {
  // 车辆基础数据缓存
  const vehicleCache = ref<Map<string, Vehicle>>(new Map());
  
  // 获取车辆基础信息
  async function getVehicleInfo(vehicleId: string): Promise<Vehicle | null> {
    if (vehicleCache.value.has(vehicleId)) {
      return vehicleCache.value.get(vehicleId)!;
    }
    
    try {
      const response = await fetch(`/api/vehicles/${vehicleId}`);
      const result = await response.json();
      
      if (result.code === 0) {
        const vehicle = result.data;
        vehicleCache.value.set(vehicleId, vehicle);
        return vehicle;
      }
    } catch (error) {
      console.error('Error fetching vehicle info:', error);
    }
    
    return null;
  }
  
  // 批量获取车辆信息
  async function getVehiclesInfo(vehicleIds: string[]): Promise<Vehicle[]> {
    const vehicles: Vehicle[] = [];
    
    for (const id of vehicleIds) {
      const vehicle = await getVehicleInfo(id);
      if (vehicle) {
        vehicles.push(vehicle);
      }
    }
    
    return vehicles;
  }
  
  // 清除缓存
  function clearCache() {
    vehicleCache.value.clear();
  }
  
  // 更新缓存中的车辆信息
  function updateVehicleCache(vehicle: Vehicle) {
    vehicleCache.value.set(vehicle.id, vehicle);
  }
  
  return {
    vehicleCache,
    getVehicleInfo,
    getVehiclesInfo,
    clearCache,
    updateVehicleCache
  };
});
