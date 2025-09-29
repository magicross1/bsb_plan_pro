// 司机数据管理

import { defineStore } from 'pinia';
import { ref } from 'vue';

export interface Driver {
  id: string;
  name: string;
  phone?: string;
  license?: string;
  status: 'active' | 'inactive' | 'busy';
}

export const useDriverStore = defineStore('driver', () => {
  // 司机列表
  const drivers = ref<Driver[]>([
    {
      id: 'DRIVER001',
      name: '张三',
      phone: '13800138001',
      license: 'A1234567',
      status: 'active'
    },
    {
      id: 'DRIVER002', 
      name: '李四',
      phone: '13800138002',
      license: 'A1234568',
      status: 'active'
    },
    {
      id: 'DRIVER003',
      name: '王五',
      phone: '13800138003',
      license: 'A1234569',
      status: 'busy'
    }
  ]);
  
  // 获取所有司机
  function getAllDrivers(): Driver[] {
    return drivers.value;
  }
  
  // 根据ID获取司机
  function getDriverById(driverId: string): Driver | null {
    return drivers.value.find(driver => driver.id === driverId) || null;
  }
  
  // 获取可用司机（状态为active且不busy）
  function getAvailableDrivers(): Driver[] {
    return drivers.value.filter(driver => driver.status === 'active');
  }
  
  // 更新司机状态
  function updateDriverStatus(driverId: string, status: Driver['status']) {
    const driver = drivers.value.find(d => d.id === driverId);
    if (driver) {
      driver.status = status;
    }
  }
  
  // 添加司机
  function addDriver(driver: Omit<Driver, 'id'>) {
    const newDriver: Driver = {
      ...driver,
      id: `DRIVER${String(drivers.value.length + 1).padStart(3, '0')}`
    };
    drivers.value.push(newDriver);
    return newDriver;
  }
  
  // 更新司机信息
  function updateDriver(driverId: string, updates: Partial<Driver>) {
    const index = drivers.value.findIndex(d => d.id === driverId);
    if (index !== -1) {
      drivers.value[index] = { ...drivers.value[index], ...updates };
    }
  }
  
  // 删除司机
  function removeDriver(driverId: string) {
    const index = drivers.value.findIndex(d => d.id === driverId);
    if (index !== -1) {
      drivers.value.splice(index, 1);
    }
  }
  
  return {
    drivers,
    getAllDrivers,
    getDriverById,
    getAvailableDrivers,
    updateDriverStatus,
    addDriver,
    updateDriver,
    removeDriver
  };
});


