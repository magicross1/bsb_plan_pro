# 数据模型定义
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List, Literal, Any

# 任务类型
TaskType = Literal[
    'Yard(F)', 'Client', 'Yard(E)', 'Empty Park',
    'Drving', 'Lifting', 'Waiting', 'Other'
]

# 时间范围
class TimeRange(BaseModel):
    startTime: datetime
    endTime: datetime

# 容器模型
class Container(BaseModel):
    ctnNumber: str = Field(alias='CTN NUMBER')
    logisticsStatus: str = Field(alias='Logitics Status')
    fullClientName: str = Field(alias='FULL CLIENT Name')
    fullDeliverAddress: str = Field(alias='FULL Deliver Address')
    deliverType: str = Field(alias='Deliver Type')
    doorPositon: str = Field(alias='Door Positon')
    fullVesselName: str = Field(alias='FULL Vessel Name')
    ctnType: str = Field(alias='CTN Type')
    ctnWeight: str = Field(alias='CTN Weight')
    remark: str = Field(alias='REMARK')
    freightForwarders: str = Field(alias='Freight Forwarders')
    terminal: str = Field(alias='Terminal')
    eta: str = Field(alias='ETA')
    etd: str = Field(alias='ETD')
    firstFree: str = Field(alias='First Free')
    lastFree: str = Field(alias='Last Free')
    lastDention: str = Field(alias='Last Dention')
    dischargeTime: str = Field(alias='Discharge Time')
    gateoutTime: str = Field(alias='Gateout Time')
    edoPin: str = Field(alias='EDO PIN')
    shippingLine: str = Field(alias='Shipping Line')
    emptyPark: str = Field(alias='Empty Park')
    pickUpDate: str = Field(alias='Pick Up Date')
    deliverDate: str = Field(alias='Deliver Date')
    pickEmptyDate: str = Field(alias='Pick Empty Date')
    dehireDate: str = Field(alias='Dehire Date')
    planPickUpDate: str = Field(alias='Plan Pick Up Date')
    planDeliverDate: str = Field(alias='Plan Deliver Date')
    planPickEmptyDate: str = Field(alias='Plan Pick Empty Date')
    planDehireDate: str = Field(alias='Plan Dehire Date')
    RequestDeliverDate: str = Field(alias='Request Deliver Date')

    class Config:
        populate_by_name = True

# 任务模型
class Task(BaseModel):
    id: str
    tripId: str
    containerNo: Optional[str] = None
    taskType: TaskType
    planStart: datetime
    planEnd: datetime
    startAddress: str
    endAddress: str
    status: Literal['pending', 'ongoing', 'completed', 'tbc'] = 'pending'
    driverId: Optional[str] = None
    vehiclePmId: Optional[str] = None
    vehicleTailId: Optional[str] = None
    containerWeight: Optional[str] = None
    containerType: Optional[str] = None

# 行程模型
class Trip(BaseModel):
    id: str
    vehicleId: str
    driverId: Optional[str] = None
    startTime: datetime
    endTime: datetime
    fullLoad: Literal['Y', 'N'] = 'N'
    tasks: List[Task] = []

# 车辆模型
class Vehicle(BaseModel):
    id: str
    plateNumber: str
    driverId: Optional[str] = None
    trips: List[Trip] = []

# 任务创建请求
class TaskCreate(BaseModel):
    tripId: Optional[str] = None
    vehicleId: Optional[str] = None
    containerNo: Optional[str] = None
    taskType: TaskType
    planStart: Optional[datetime] = None
    planEnd: Optional[datetime] = None

# 行程创建请求
class TripCreate(BaseModel):
    vehicleId: str
    driverId: Optional[str] = None
    startTime: datetime
    endTime: datetime
    fullLoad: Literal['Y', 'N'] = 'N'

# 拖拽改变车辆请求
class DragPmPayload(BaseModel):
    tripId: str
    newPmId: str
    newStartTime: datetime

# 拖拽改变时间请求
class DragTimePayload(BaseModel):
    tripId: str
    newStart: datetime
    newEnd: datetime

# 车辆刷新请求
class VehicleRefreshRequest(BaseModel):
    vehicleIds: List[str]
    range: Optional[TimeRange] = None

# API响应格式
class ApiResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

# 时间查询格式
class DateRequest(BaseModel):
    query_date: date