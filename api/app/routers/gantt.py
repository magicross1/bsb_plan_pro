# 甘特图相关API路由
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from typing import List, Optional
from app.models import (
    ApiResponse, TimeRange, TaskCreate, TripCreate, 
    DragPmPayload, DragTimePayload, VehicleRefreshRequest
)
from app.database import (
    get_vehicles_by_time_range, add_task, delete_task, 
    add_trip, delete_trip, update_trip_pm, update_trip_time
)

router = APIRouter()

@router.get("/vehicles")
async def get_vehicles(start: str, end: str):
    """获取车辆列表"""
    try:
        vehicles = get_vehicles_by_time_range(start, end)
        return ApiResponse(
            code=0,
            message="ok",
            data=[vehicle.dict() for vehicle in vehicles]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车辆列表失败: {str(e)}")

@router.post("/vehicles/refresh")
async def refresh_vehicles(request: VehicleRefreshRequest):
    """刷新车辆数据"""
    try:
        if request.range:
            vehicles = get_vehicles_by_time_range(
                request.range.startTime.strftime('%Y-%m-%d %H:%M:%S'),
                request.range.endTime.strftime('%Y-%m-%d %H:%M:%S')
            )
        else:
            # 默认时间范围
            now = datetime.now()
            start = (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            end = (now + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
            vehicles = get_vehicles_by_time_range(start, end)
        
        # 过滤指定车辆
        filtered_vehicles = [
            vehicle for vehicle in vehicles 
            if vehicle.id in request.vehicleIds
        ]
        
        return ApiResponse(
            code=0,
            message="ok",
            data=[vehicle.dict() for vehicle in filtered_vehicles]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刷新车辆数据失败: {str(e)}")

@router.get("/trip/{trip_id}")
async def get_trip(trip_id: str):
    """获取行程详情"""
    try:
        from app.database import DB
        
        trip_data = None
        for trip in DB['trips']:
            if trip['id'] == trip_id:
                trip_data = trip
                break
        
        if not trip_data:
            raise HTTPException(status_code=404, detail="行程不存在")
        
        # 获取相关任务
        tasks = [task for task in DB['tasks'] if task['tripId'] == trip_id]
        trip_data['tasks'] = tasks
        
        return ApiResponse(code=0, message="ok", data=trip_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取行程详情失败: {str(e)}")

@router.post("/task")
async def create_task(task_data: TaskCreate):
    """创建任务"""
    try:
        # 验证行程是否存在且未满载
        from app.database import DB
        
        trip = None
        for t in DB['trips']:
            if t['id'] == task_data.tripId:
                trip = t
                break
        
        if not trip:
            return ApiResponse(code=40002, message="行程不存在", data=None)
        
        if trip['fullLoad'] == 'Y':
            return ApiResponse(code=40002, message="行程已满载，无法添加任务", data=None)
        
        # 检查任务数量限制
        existing_tasks = [task for task in DB['tasks'] if task['tripId'] == task_data.tripId]
        if len(existing_tasks) >= 2:
            return ApiResponse(code=40002, message="行程任务数量已达上限", data=None)
        
        # 创建任务
        import uuid
        task_dict = {
            'id': str(uuid.uuid4()),
            'tripId': task_data.tripId,
            'containerNo': task_data.containerNo,
            'taskType': task_data.taskType,
            'planStart': (task_data.planStart or datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
            'planEnd': (task_data.planEnd or datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
            'startAddress': '',
            'endAddress': '',
            'status': 'pending'
        }
        
        task = add_task(task_dict)
        
        return ApiResponse(code=0, message="ok", data=task.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")

@router.delete("/task/{task_id}")
async def delete_task_endpoint(task_id: str):
    """删除任务"""
    try:
        success = delete_task(task_id)
        if success:
            return ApiResponse(code=0, message="ok", data=None)
        else:
            return ApiResponse(code=404, message="任务不存在", data=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")

@router.post("/drag/pm")
async def drag_change_pm(payload: DragPmPayload):
    """拖拽改变车辆"""
    try:
        # 验证目标车辆存在
        from app.database import DB
        
        target_vehicle = None
        for vehicle in DB['vehicles']:
            if vehicle['id'] == payload.newPmId:
                target_vehicle = vehicle
                break
        
        if not target_vehicle:
            return ApiResponse(code=40003, message="目标车辆不存在", data=None)
        
        # 更新行程车辆
        success = update_trip_pm(payload.tripId, payload.newPmId, payload.newStartTime)
        
        if success:
            return ApiResponse(code=0, message="ok", data=None)
        else:
            return ApiResponse(code=404, message="行程不存在", data=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"拖拽改变车辆失败: {str(e)}")

@router.post("/trip")
async def create_trip(trip_data: TripCreate):
    """创建行程"""
    try:
        import uuid
        trip_dict = {
            'id': str(uuid.uuid4()),
            'vehicleId': trip_data.vehicleId,
            'driverId': trip_data.driverId,
            'startTime': trip_data.startTime.strftime('%Y-%m-%d %H:%M:%S'),
            'endTime': trip_data.endTime.strftime('%Y-%m-%d %H:%M:%S'),
            'fullLoad': trip_data.fullLoad
        }
        
        trip = add_trip(trip_dict)
        
        return ApiResponse(code=0, message="ok", data=trip.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建行程失败: {str(e)}")

@router.delete("/trip/{trip_id}")
async def delete_trip_endpoint(trip_id: str):
    """删除行程"""
    try:
        success = delete_trip(trip_id)
        if success:
            return ApiResponse(code=0, message="ok", data=None)
        else:
            return ApiResponse(code=404, message="行程不存在", data=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除行程失败: {str(e)}")

@router.post("/drag/time")
async def drag_change_trip_time(payload: DragTimePayload):
    """拖拽改变时间"""
    try:
        # 验证时间有效性
        if payload.newStart >= payload.newEnd:
            return ApiResponse(code=40001, message="开始时间必须早于结束时间", data=None)
        
        # 更新行程时间
        success = update_trip_time(payload.tripId, payload.newStart, payload.newEnd)
        
        if success:
            return ApiResponse(code=0, message="ok", data=None)
        else:
            return ApiResponse(code=404, message="行程不存在", data=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"拖拽改变时间失败: {str(e)}")

@router.get("/get_vehicle_driver_list")
async def get_vehicle_driver_list():
    try:
        from app.database import DB

        # 所有车辆和司机
        plateNumber = DB['plateNumber']
        driverId = DB['driverId']

        # 已创建的车辆和司机
        vehicles = DB['vehicles']
        selected_vehicles = [vehicle['plateNumber'] for vehicle in vehicles]
        selected_drivers = [vehicle['driverId'] for vehicle in vehicles]

        # 返回可选择的车辆和司机
        availableVehicles = [v for v in plateNumber if v not in selected_vehicles]
        availableDrivers = [d for d in driverId if d not in selected_drivers]
        
        return ApiResponse(code=0, message="ok", data=[availableVehicles, availableDrivers])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取车辆列表失败: {str(e)}")