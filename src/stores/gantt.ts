// 甘特图核心状态管理

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { 
  Vehicle, 
  Trip, 
  Task, 
  GanttSettings, 
  ContextMenu, 
  ViewMode, 
  TimeRange,
  ApiResponse 
} from '@/types';
import { getCurrentTime, getDefaultTimeRange } from '@/utils/time';

export const useGanttStore = defineStore('gantt', () => {
  // 时间轴设置
  const timelineStart = ref<string>(getDefaultTimeRange().start);
  const timelineEnd = ref<string>(getDefaultTimeRange().end);
  const pixelsPerHour = ref<number>(100);

  // 车辆数据
  const vehicles = ref<Vehicle[]>([]);
  
  // 选中的任务
  const selectedTasks = ref<string[]>([]);
  
  // 上下文菜单
  const contextMenu = ref<ContextMenu>({
    visible: false,
    x: 0,
    y: 0,
    type: 'blank',
    payload: null
  });

  // 设置
  const settings = ref<GanttSettings>({
    rowHeight: 60,
    taskMargin: 4,
    tripBackgroundColor: '#e3f2fd',
    showCurrentTime: true,
    collab: {
      enabled: false,
      intervalSec: 30,
      visibleOnly: true
    }
  });

  // 视图模式
  const viewMode = ref<ViewMode>('horizontal');

  // 计算属性
  const minutesPerPixel = computed(() => 60 / pixelsPerHour.value);
  
  const timelineWidth = computed(() => {
    const start = new Date(timelineStart.value);
    const end = new Date(timelineEnd.value);
    const diffMinutes = (end.getTime() - start.getTime()) / (1000 * 60);
    return diffMinutes / minutesPerPixel.value;
  });

  // 时间转像素
  function timeToPx(time: string | Date): number {
    const minutesPerPixel = 60 / pixelsPerHour.value;
    const diffMinutes = new Date(time).getTime() - new Date(timelineStart.value).getTime();
    return diffMinutes / (1000 * 60) / minutesPerPixel;
  }

  // 像素转时间
  function pxToTime(pixels: number): string {
    const minutesPerPixel = 60 / pixelsPerHour.value;
    const diffMinutes = pixels * minutesPerPixel;
    const newTime = new Date(new Date(timelineStart.value).getTime() + diffMinutes * 60 * 1000);
    return newTime.toISOString().slice(0, 19).replace('T', ' ');
  }

  // 获取车辆列表
  async function fetchVehicleList(range?: TimeRange) {
    try {
      const params = new URLSearchParams();
      if (range) {
        params.append('start', range.start);
        params.append('end', range.end);
      } else {
        params.append('start', timelineStart.value);
        params.append('end', timelineEnd.value);
      }
      
      const response = await fetch(`/api/gantt/vehicles?${params}`);
      const result: ApiResponse<Vehicle[]> = await response.json();
      
      if (result.code === 0) {
        vehicles.value = result.data;
      } else {
        console.error('Failed to fetch vehicles:', result.message);
      }
    } catch (error) {
      console.error('Error fetching vehicles:', error);
    }
  }

  // 更新车辆数据
  async function updateVehicleData(vehicleIds: string[], range?: TimeRange) {
    try {
      const response = await fetch('/api/gantt/vehicles/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vehicleIds,
          range: range || { start: timelineStart.value, end: timelineEnd.value }
        })
      });
      
      const result: ApiResponse<Vehicle[]> = await response.json();
      
      if (result.code === 0) {
        // 更新对应车辆的数据
        result.data.forEach(updatedVehicle => {
          const index = vehicles.value.findIndex(v => v.id === updatedVehicle.id);
          if (index !== -1) {
            vehicles.value[index] = updatedVehicle;
          }
        });
      }
    } catch (error) {
      console.error('Error updating vehicle data:', error);
    }
  }

  // 添加行程
  async function addTrip(vehicleId: string, payload: Partial<Trip>) {
    try {
      const response = await fetch('/api/gantt/trip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vehicleId,
          ...payload
        })
      });
      
      const result: ApiResponse<Trip> = await response.json();
      
      if (result.code === 0) {
        const vehicle = vehicles.value.find(v => v.id === vehicleId);
        if (vehicle) {
          vehicle.trips.push(result.data);
        }
        return result.data;
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      console.error('Error adding trip:', error);
      throw error;
    }
  }

  // 添加任务
  async function addTask(tripId: string, payload: Partial<Task>) {
    try {
      const response = await fetch('/api/gantt/task', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tripId,
          ...payload
        })
      });
      
      const result: ApiResponse<Task> = await response.json();
      
      if (result.code === 0) {
        // 找到对应的行程并添加任务
        vehicles.value.forEach(vehicle => {
          const trip = vehicle.trips.find(t => t.id === tripId);
          if (trip) {
            trip.tasks.push(result.data);
          }
        });
        return result.data;
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      console.error('Error adding task:', error);
      throw error;
    }
  }

  // 删除任务
  async function deleteTask(taskId: string) {
    try {
      const response = await fetch(`/api/gantt/task/${taskId}`, {
        method: 'DELETE'
      });
      
      const result: ApiResponse = await response.json();
      
      if (result.code === 0) {
        // 从车辆数据中移除任务
        vehicles.value.forEach(vehicle => {
          vehicle.trips.forEach(trip => {
            trip.tasks = trip.tasks.filter(task => task.id !== taskId);
          });
        });
        
        // 从选中任务中移除
        selectedTasks.value = selectedTasks.value.filter(id => id !== taskId);
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }

  // 删除行程
  async function deleteTrip(tripId: string) {
    try {
      const response = await fetch(`/api/gantt/trip/${tripId}`, {
        method: 'DELETE'
      });
      
      const result: ApiResponse = await response.json();
      
      if (result.code === 0) {
        // 从车辆数据中移除行程及其任务
        vehicles.value.forEach(vehicle => {
          const trip = vehicle.trips.find(t => t.id === tripId);
          if (trip) {
            // 移除相关任务的选择状态
            trip.tasks.forEach(task => {
              selectedTasks.value = selectedTasks.value.filter(id => id !== task.id);
            });
            // 移除行程
            vehicle.trips = vehicle.trips.filter(t => t.id !== tripId);
          }
        });
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      console.error('Error deleting trip:', error);
      throw error;
    }
  }

  // 拖拽改变车辆
  async function dragChangePm({ tripId, newPmId, newStartTime }: {
    tripId: string;
    newPmId: string;
    newStartTime: string;
  }) {
    try {
      const response = await fetch('/api/gantt/drag/pm', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tripId,
          newPmId,
          newStartTime
        })
      });
      
      const result: ApiResponse = await response.json();
      
      if (result.code === 0) {
        // 刷新车辆数据
        await fetchVehicleList();
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      console.error('Error changing PM:', error);
      throw error;
    }
  }

  // 拖拽改变时间
  async function dragChangeTripTime({ tripId, newStart, newEnd }: {
    tripId: string;
    newStart: string;
    newEnd: string;
  }) {
    try {
      const response = await fetch('/api/gantt/drag/time', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tripId,
          newStart,
          newEnd
        })
      });
      
      const result: ApiResponse = await response.json();
      
      if (result.code === 0) {
        // 更新本地数据
        vehicles.value.forEach(vehicle => {
          const trip = vehicle.trips.find(t => t.id === tripId);
          if (trip) {
            trip.startTime = newStart;
            trip.endTime = newEnd;
          }
        });
      } else {
        throw new Error(result.message);
      }
    } catch (error) {
      console.error('Error changing trip time:', error);
      throw error;
    }
  }

  // 持久化设置
  function persistSettings() {
    localStorage.setItem('gantt_settings', JSON.stringify(settings.value));
  }

  // 加载设置
  function loadSettings() {
    const saved = localStorage.getItem('gantt_settings');
    if (saved) {
      try {
        settings.value = { ...settings.value, ...JSON.parse(saved) };
      } catch (error) {
        console.error('Error loading settings:', error);
      }
    }
  }

  // 显示上下文菜单
  function showContextMenu(x: number, y: number, type: ContextMenu['type'], payload?: any) {
    contextMenu.value = {
      visible: true,
      x,
      y,
      type,
      payload
    };
  }

  // 隐藏上下文菜单
  function hideContextMenu() {
    contextMenu.value.visible = false;
  }

  // 切换视图模式
  function toggleViewMode() {
    viewMode.value = viewMode.value === 'horizontal' ? 'vertical' : 'horizontal';
  }

  return {
    // 状态
    timelineStart,
    timelineEnd,
    pixelsPerHour,
    vehicles,
    selectedTasks,
    contextMenu,
    settings,
    viewMode,
    
    // 计算属性
    minutesPerPixel,
    timelineWidth,
    
    // 方法
    timeToPx,
    pxToTime,
    fetchVehicleList,
    updateVehicleData,
    addTrip,
    addTask,
    deleteTask,
    deleteTrip,
    dragChangePm,
    dragChangeTripTime,
    persistSettings,
    loadSettings,
    showContextMenu,
    hideContextMenu,
    toggleViewMode
  };
});
