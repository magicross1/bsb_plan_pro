// BSB调度甘特系统 - 类型定义

// 任务类型定义
export const TaskTypes = [
  'Yard(F)', 'Client', 'Yard(E)', 'Empty Park',
  'Drving', 'Lifting', 'Waiting', 'Other'
] as const;

export type TaskType = typeof TaskTypes[number];

// 容器接口（映射业务数据）
export interface Container {
  ctnNumber: string;               // 映射 'CTN NUMBER'
  logisticsStatus: string;         // 'Logitics Status'
  fullClientName: string;          // 'FULL CLIENT Name'
  fullDeliverAddress: string;      // 'FULL Deliver Address'
  deliverType: string;             // 'Deliver Type'
  doorPositon: string;             // 'Door Positon'
  fullVesselName: string;          // 'FULL Vessel Name'
  ctnType: string;                 // 'CTN Type'
  ctnWeight: string;               // 'CTN Weight'
  remark: string;                  // 'REMARK'
  freightForwarders: string;       // 'Freight Forwarders'
  terminal: string;                // 'Terminal'
  eta: string; 
  etd: string;                     // 'ETD'
  firstFree: string; 
  lastFree: string; 
  lastDention: string;
  dischargeTime: string; 
  gateoutTime: string;
  edoPin: string; 
  shippingLine: string;
  emptyPark: string;
  pickUpDate: string; 
  deliverDate: string; 
  pickEmptyDate: string; 
  dehireDate: string;
  planPickUpDate: string; 
  planDeliverDate: string; 
  planPickEmptyDate: string; 
  planDehireDate: string;
}

// 车辆接口
export interface Vehicle {
  id: string;                      // PM 车头ID
  plateNumber: string;
  driverId?: string;
  trips: Trip[];
}

// 行程接口
export interface Trip {
  id: string;
  vehicleId: string;
  driverId?: string;
  startTime: string;               // YYYY-MM-DD HH:mm:ss
  endTime: string;
  fullLoad: 'Y' | 'N';
  tasks: Task[];                   // 最多 2 个任务；fullLoad === 'Y' 禁止新增
}

// 任务接口
export interface Task {
  id: string;
  tripId: string;
  containerNo?: string;            // 对应 Container.ctnNumber
  taskType: TaskType;              // D/L/U/M 等映射见视觉
  planStart: string;
  planEnd: string;
  startAddress: string;
  endAddress: string;
  status: 'pending' | 'ongoing' | 'completed' | 'tbc';
  driverId?: string;
  vehiclePmId?: string;
  vehicleTailId?: string;
  containerWeight?: string;
  containerType?: string;
}

// 甘特图设置
export interface GanttSettings {
  rowHeight: number;
  taskMargin: number;
  tripBackgroundColor: string;
  showCurrentTime: boolean;
  collab: {
    enabled: boolean;
    intervalSec: number;
    visibleOnly: boolean;
  };
}

// 上下文菜单
export interface ContextMenu {
  visible: boolean;
  x: number;
  y: number;
  type: 'blank' | 'track' | 'trip' | 'task';
  payload?: any;
}

// 视图模式
export type ViewMode = 'horizontal' | 'vertical';

// 时间范围
export interface TimeRange {
  start: string;
  end: string;
}

// API响应格式
export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}
