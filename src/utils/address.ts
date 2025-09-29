// 地址生成工具函数

import type { Container, TaskType } from '@/types';

/**
 * 获取取货地址
 */
export function getPickupAddress(container: Container): string {
  const status = container.logisticsStatus;
  
  if (status === '新订单') return container.terminal;
  if (status === 'Yard(F)') return `${container.fullClientName} - Ready to Deliver`;
  if (status === 'Client') return container.fullDeliverAddress;
  if (status === 'Yard(E)') return `${container.fullClientName} - Ready to De-hire`;
  if (status === 'Empty Park') return container.emptyPark;
  
  return container.terminal;
}

/**
 * 获取送货地址
 */
export function getDeliveryAddress(taskType: TaskType, container: Container): string {
  const addressMap: Record<TaskType, string> = {
    'Yard(F)': `${container.fullClientName} - Ready to Deliver`,
    'Client': container.fullDeliverAddress,
    'Yard(E)': `${container.fullClientName} - Ready to De-hire`,
    'Empty Park': container.emptyPark,
    'Drving': 'In Transit',
    'Lifting': 'Lifting Location',
    'Waiting': 'Waiting Area',
    'Other': 'Other Location',
  };
  
  return addressMap[taskType] || container.fullDeliverAddress;
}
