// 任务类型管理

import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { TaskType } from '@/types';

export const useTaskTypeStore = defineStore('taskType', () => {
  // 任务类型颜色映射
  const taskTypeColors = ref<Record<TaskType, string>>({
    'Yard(F)': '#4caf50',      // 绿色
    'Client': '#2196f3',       // 蓝色
    'Yard(E)': '#ff9800',      // 橙色
    'Empty Park': '#9c27b0',   // 紫色
    'Drving': '#f44336',       // 红色
    'Lifting': '#795548',      // 棕色
    'Waiting': '#607d8b',      // 蓝灰色
    'Other': '#9e9e9e'         // 灰色
  });

  // 任务类型图标映射
  const taskTypeIcons = ref<Record<TaskType, string>>({
    'Yard(F)': 'truck',
    'Client': 'user',
    'Yard(E)': 'warehouse',
    'Empty Park': 'parking',
    'Drving': 'car',
    'Lifting': 'crane',
    'Waiting': 'clock',
    'Other': 'ellipsis'
  });

  // 任务类型描述
  const taskTypeDescriptions = ref<Record<TaskType, string>>({
    'Yard(F)': '满载货场',
    'Client': '客户送货',
    'Yard(E)': '空载货场',
    'Empty Park': '空柜停放',
    'Drving': '运输途中',
    'Lifting': '装卸作业',
    'Waiting': '等待作业',
    'Other': '其他任务'
  });

  // 获取任务类型颜色
  function getTaskTypeColor(taskType: TaskType): string {
    return taskTypeColors.value[taskType] || '#9e9e9e';
  }

  // 获取任务类型图标
  function getTaskTypeIcon(taskType: TaskType): string {
    return taskTypeIcons.value[taskType] || 'ellipsis';
  }

  // 获取任务类型描述
  function getTaskTypeDescription(taskType: TaskType): string {
    return taskTypeDescriptions.value[taskType] || '未知类型';
  }

  // 获取所有任务类型配置
  function getAllTaskTypes() {
    return Object.keys(taskTypeColors.value).map(type => ({
      type: type as TaskType,
      color: taskTypeColors.value[type as TaskType],
      icon: taskTypeIcons.value[type as TaskType],
      description: taskTypeDescriptions.value[type as TaskType]
    }));
  }

  return {
    taskTypeColors,
    taskTypeIcons,
    taskTypeDescriptions,
    getTaskTypeColor,
    getTaskTypeIcon,
    getTaskTypeDescription,
    getAllTaskTypes
  };
});
