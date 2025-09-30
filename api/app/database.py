# 内存数据库实现
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid
from app.models import Vehicle, Trip, Task, Container

# 内存数据存储
DB = {
    'vehicles': [],
    'trips': [],
    'tasks': [],
    'containers': []
}

def init_sample_data():
    """初始化示例数据"""
    # 创建示例车辆
    vehicles = [
        {
            'id': 'PM001',
            'plateNumber': 'ABC-123',
            'driverId': 'DRIVER001',
            'trips': []
        },
        {
            'id': 'PM002', 
            'plateNumber': 'DEF-456',
            'driverId': 'DRIVER002',
            'trips': []
        },
        {
            'id': 'PM003',
            'plateNumber': 'GHI-789',
            'driverId': None,
            'trips': []
        }
    ]
    
    # 创建示例容器
    containers = [
        {
            'CTN NUMBER': 'CONT001',
            'Logitics Status': '新订单',
            'FULL CLIENT Name': '客户A',
            'FULL Deliver Address': '悉尼港码头',
            'Deliver Type': 'Full',
            'Door Positon': 'A1',
            'FULL Vessel Name': '货轮A',
            'CTN Type': '20GP',
            'CTN Weight': '15000',
            'REMARK': '紧急',
            'Freight Forwarders': '物流公司A',
            'Terminal': '悉尼港',
            'ETA': '2024-01-15 08:00:00',
            'ETD': '2024-01-20 16:00:00',
            'First Free': '2024-01-16 00:00:00',
            'Last Free': '2024-01-18 23:59:59',
            'Last Dention': '2024-01-19 00:00:00',
            'Discharge Time': '2024-01-15 10:00:00',
            'Gateout Time': '2024-01-15 12:00:00',
            'EDO PIN': 'PIN001',
            'Shipping Line': '航运公司A',
            'Empty Park': '空柜场A',
            'Pick Up Date': '2024-01-16 09:00:00',
            'Deliver Date': '2024-01-16 14:00:00',
            'Pick Empty Date': '2024-01-18 10:00:00',
            'Dehire Date': '2024-01-18 15:00:00',
            'Plan Pick Up Date': '2024-01-16 09:00:00',
            'Plan Deliver Date': '2024-01-16 14:00:00',
            'Plan Pick Empty Date': '2024-01-18 10:00:00',
            'Plan Dehire Date': '2024-01-18 15:00:00',
            'Request Deliver Date': '',
        },
        {
            'CTN NUMBER': 'CONT002',
            'Logitics Status': 'Client',
            'FULL CLIENT Name': '客户B',
            'FULL Deliver Address': '墨尔本仓库',
            'Deliver Type': 'Empty',
            'Door Positon': 'B2',
            'FULL Vessel Name': '货轮B',
            'CTN Type': '40HQ',
            'CTN Weight': '20000',
            'REMARK': '普通',
            'Freight Forwarders': '物流公司B',
            'Terminal': '墨尔本港',
            'ETA': '2024-01-16 06:00:00',
            'ETD': '2024-01-22 18:00:00',
            'First Free': '2024-01-17 00:00:00',
            'Last Free': '2024-01-19 23:59:59',
            'Last Dention': '2024-01-20 00:00:00',
            'Discharge Time': '2024-01-16 08:00:00',
            'Gateout Time': '2024-01-16 10:00:00',
            'EDO PIN': 'PIN002',
            'Shipping Line': '航运公司B',
            'Empty Park': '空柜场B',
            'Pick Up Date': '2024-01-17 08:00:00',
            'Deliver Date': '2024-01-17 12:00:00',
            'Pick Empty Date': '2024-01-19 09:00:00',
            'Dehire Date': '2024-01-19 14:00:00',
            'Plan Pick Up Date': '2024-01-17 08:00:00',
            'Plan Deliver Date': '2024-01-17 12:00:00',
            'Plan Pick Empty Date': '2024-01-19 09:00:00',
            'Plan Dehire Date': '2024-01-19 14:00:00',
            'Request Deliver Date': '',
        },
        {
            'CTN NUMBER': 'CONT003',
            'Logitics Status': 'Client',
            'FULL CLIENT Name': '客户B',
            'FULL Deliver Address': '墨尔本仓库',
            'Deliver Type': 'Empty',
            'Door Positon': 'B2',
            'FULL Vessel Name': '货轮B',
            'CTN Type': '40HQ',
            'CTN Weight': '20000',
            'REMARK': '普通',
            'Freight Forwarders': '物流公司B',
            'Terminal': '墨尔本港',
            'ETA': '2024-01-16 06:00:00',
            'ETD': '2024-01-22 18:00:00',
            'First Free': '2024-01-17 00:00:00',
            'Last Free': '2025-09-30 23:59:59',
            'Last Dention': '2025-09-30 00:00:00',
            'Discharge Time': '2024-01-16 08:00:00',
            'Gateout Time': '2024-01-16 10:00:00',
            'EDO PIN': 'PIN002',
            'Shipping Line': '航运公司B',
            'Empty Park': '空柜场B',
            'Pick Up Date': '2024-01-17 08:00:00',
            'Deliver Date': '2024-01-17 12:00:00',
            'Pick Empty Date': '2024-01-19 09:00:00',
            'Dehire Date': '2024-01-19 14:00:00',
            'Plan Pick Up Date': '',
            'Plan Deliver Date': '2024-01-17 12:00:00',
            'Plan Pick Empty Date': '2024-01-19 09:00:00',
            'Plan Dehire Date': '2024-01-19 14:00:00',
            'Request Deliver Date': '',
        },
        {
            'CTN NUMBER': 'CONT004',
            'Logitics Status': 'Client',
            'FULL CLIENT Name': '客户B',
            'FULL Deliver Address': '墨尔本仓库',
            'Deliver Type': 'Empty',
            'Door Positon': 'B2',
            'FULL Vessel Name': '货轮B',
            'CTN Type': '40HQ',
            'CTN Weight': '20000',
            'REMARK': '普通',
            'Freight Forwarders': '物流公司B',
            'Terminal': '墨尔本港',
            'ETA': '2024-01-16 06:00:00',
            'ETD': '2024-01-22 18:00:00',
            'First Free': '2024-01-17 00:00:00',
            'Last Free': '2025-09-30 23:59:59',
            'Last Dention': '2024-01-20 00:00:00',
            'Discharge Time': '2024-01-16 08:00:00',
            'Gateout Time': '2024-01-16 10:00:00',
            'EDO PIN': 'PIN002',
            'Shipping Line': '航运公司B',
            'Empty Park': '空柜场B',
            'Pick Up Date': '2024-01-17 08:00:00',
            'Deliver Date': '2024-01-17 12:00:00',
            'Pick Empty Date': '2024-01-19 09:00:00',
            'Dehire Date': '2024-01-19 14:00:00',
            'Plan Pick Up Date': '2025-10-30 08:00:00',
            'Plan Deliver Date': '2024-01-17 12:00:00',
            'Plan Pick Empty Date': '2024-01-19 09:00:00',
            'Plan Dehire Date': '2024-01-19 14:00:00',
            'Request Deliver Date': '',
        },
        {
            'CTN NUMBER': 'CONT005',
            'Logitics Status': 'Client',
            'FULL CLIENT Name': '客户B',
            'FULL Deliver Address': '墨尔本仓库',
            'Deliver Type': 'Empty',
            'Door Positon': 'B2',
            'FULL Vessel Name': '货轮B',
            'CTN Type': '40HQ',
            'CTN Weight': '20000',
            'REMARK': '普通',
            'Freight Forwarders': '物流公司B',
            'Terminal': '墨尔本港',
            'ETA': '2024-01-16 06:00:00',
            'ETD': '2024-01-22 18:00:00',
            'First Free': '2024-01-17 00:00:00',
            'Last Free': '2025-09-30 23:59:59',
            'Last Dention': '2025-09-30 00:00:00',
            'Discharge Time': '2024-01-16 08:00:00',
            'Gateout Time': '2024-01-16 10:00:00',
            'EDO PIN': 'PIN002',
            'Shipping Line': '航运公司B',
            'Empty Park': '空柜场B',
            'Pick Up Date': '2024-01-17 08:00:00',
            'Deliver Date': '2024-01-17 12:00:00',
            'Pick Empty Date': '2024-01-19 09:00:00',
            'Dehire Date': '2024-01-19 14:00:00',
            'Plan Pick Up Date': '2025-10-30 08:00:00',
            'Plan Deliver Date': '2024-01-17 12:00:00',
            'Plan Pick Empty Date': '2024-01-19 09:00:00',
            'Plan Dehire Date': '',
            'Request Deliver Date': '',
        },
        {
            'CTN NUMBER': 'CONT006',
            'Logitics Status': 'Client',
            'FULL CLIENT Name': '客户B',
            'FULL Deliver Address': '墨尔本仓库',
            'Deliver Type': 'Empty',
            'Door Positon': 'B2',
            'FULL Vessel Name': '货轮B',
            'CTN Type': '40HQ',
            'CTN Weight': '20000',
            'REMARK': '普通',
            'Freight Forwarders': '物流公司B',
            'Terminal': '墨尔本港',
            'ETA': '2024-01-16 06:00:00',
            'ETD': '2024-01-22 18:00:00',
            'First Free': '2024-01-17 00:00:00',
            'Last Free': '2025-09-30 23:59:59',
            'Last Dention': '2025-09-30 00:00:00',
            'Discharge Time': '2024-01-16 08:00:00',
            'Gateout Time': '2024-01-16 10:00:00',
            'EDO PIN': 'PIN002',
            'Shipping Line': '航运公司B',
            'Empty Park': '空柜场B',
            'Pick Up Date': '2024-01-17 08:00:00',
            'Deliver Date': '2024-01-17 12:00:00',
            'Pick Empty Date': '2024-01-19 09:00:00',
            'Dehire Date': '2024-01-19 14:00:00',
            'Plan Pick Up Date': '2025-10-30 08:00:00',
            'Plan Deliver Date': '2024-01-17 12:00:00',
            'Plan Pick Empty Date': '2024-01-19 09:00:00',
            'Plan Dehire Date': '2025-10-30 08:00:00',
            'Request Deliver Date': '',
        },
        {
            'CTN NUMBER': '客户要求柜子测试1-无plan deliver',
            'Logitics Status': 'Client',
            'FULL CLIENT Name': '客户B',
            'FULL Deliver Address': '墨尔本仓库',
            'Deliver Type': 'Empty',
            'Door Positon': 'B2',
            'FULL Vessel Name': '货轮B',
            'CTN Type': '40HQ',
            'CTN Weight': '20000',
            'REMARK': '普通',
            'Freight Forwarders': '物流公司B',
            'Terminal': '墨尔本港',
            'ETA': '2024-01-16 06:00:00',
            'ETD': '2024-01-22 18:00:00',
            'First Free': '2024-01-17 00:00:00',
            'Last Free': '2025-09-30 23:59:59',
            'Last Dention': '2025-09-30 00:00:00',
            'Discharge Time': '2024-01-16 08:00:00',
            'Gateout Time': '2024-01-16 10:00:00',
            'EDO PIN': 'PIN002',
            'Shipping Line': '航运公司B',
            'Empty Park': '空柜场B',
            'Pick Up Date': '2024-01-17 08:00:00',
            'Deliver Date': '2024-01-17 12:00:00',
            'Pick Empty Date': '2024-01-19 09:00:00',
            'Dehire Date': '2024-01-19 14:00:00',
            'Plan Pick Up Date': '2025-10-30 08:00:00',
            'Plan Deliver Date': '',
            'Plan Pick Empty Date': '2024-01-19 09:00:00',
            'Plan Dehire Date': '2025-10-30 08:00:00',
            'Request Deliver Date': '2025-09-30 00:00:00',
        },
        {
            'CTN NUMBER': '客户要求柜子测试2-plan deliver与request不同',
            'Logitics Status': 'Client',
            'FULL CLIENT Name': '客户B',
            'FULL Deliver Address': '墨尔本仓库',
            'Deliver Type': 'Empty',
            'Door Positon': 'B2',
            'FULL Vessel Name': '货轮B',
            'CTN Type': '40HQ',
            'CTN Weight': '20000',
            'REMARK': '普通',
            'Freight Forwarders': '物流公司B',
            'Terminal': '墨尔本港',
            'ETA': '2024-01-16 06:00:00',
            'ETD': '2024-01-22 18:00:00',
            'First Free': '2024-01-17 00:00:00',
            'Last Free': '2025-09-30 23:59:59',
            'Last Dention': '2025-09-30 00:00:00',
            'Discharge Time': '2024-01-16 08:00:00',
            'Gateout Time': '2024-01-16 10:00:00',
            'EDO PIN': 'PIN002',
            'Shipping Line': '航运公司B',
            'Empty Park': '空柜场B',
            'Pick Up Date': '2024-01-17 08:00:00',
            'Deliver Date': '2024-01-17 12:00:00',
            'Pick Empty Date': '2024-01-19 09:00:00',
            'Dehire Date': '2024-01-19 14:00:00',
            'Plan Pick Up Date': '2025-10-30 08:00:00',
            'Plan Deliver Date': '2025-10-30 08:00:00',
            'Plan Pick Empty Date': '2024-01-19 09:00:00',
            'Plan Dehire Date': '2025-10-30 08:00:00',
            'Request Deliver Date': '2025-09-30 00:00:00',
        }
    ]
    
    # 创建示例行程和任务
    now = datetime.now()
    
    # 为PM001创建行程和任务
    trip1 = {
        'id': str(uuid.uuid4()),
        'vehicleId': 'PM001',
        'driverId': 'DRIVER001',
        'startTime': (now + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
        'endTime': (now + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
        'fullLoad': 'N'
    }
    
    task1 = {
        'id': str(uuid.uuid4()),
        'tripId': trip1['id'],
        'containerNo': 'CONT001',
        'taskType': 'Client',
        'planStart': (now + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
        'planEnd': (now + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
        'startAddress': '悉尼港码头',
        'endAddress': '客户A仓库',
        'status': 'pending'
    }
    
    task2 = {
        'id': str(uuid.uuid4()),
        'tripId': trip1['id'],
        'containerNo': 'CONT002',
        'taskType': 'Empty Park',
        'planStart': (now + timedelta(hours=2, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
        'planEnd': (now + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'),
        'startAddress': '客户A仓库',
        'endAddress': '空柜场A',
        'status': 'pending'
    }
    
    # 更新数据
    DB['vehicles'] = vehicles
    DB['containers'] = containers
    DB['trips'].append(trip1)
    DB['tasks'].extend([task1, task2])
    
    # 更新车辆行程关系
    for vehicle in DB['vehicles']:
        if vehicle['id'] == 'PM001':
            vehicle['trips'] = [trip1]
            break

def get_vehicles_by_time_range(start_time: str, end_time: str) -> List[Vehicle]:
    """根据时间范围获取车辆数据"""
    vehicles = []
    
    for vehicle_data in DB['vehicles']:
        vehicle_trips = []
        
        for trip_data in DB['trips']:
            if trip_data['vehicleId'] == vehicle_data['id']:
                # 检查行程是否在时间范围内
                trip_start = datetime.strptime(trip_data['startTime'], '%Y-%m-%d %H:%M:%S')
                trip_end = datetime.strptime(trip_data['endTime'], '%Y-%m-%d %H:%M:%S')
                range_start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                range_end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                
                # 如果行程与时间范围有重叠
                if not (trip_end <= range_start or trip_start >= range_end):
                    trip_tasks = []
                    for task_data in DB['tasks']:
                        if task_data['tripId'] == trip_data['id']:
                            task = Task(**task_data)
                            trip_tasks.append(task)
                    
                    trip = Trip(
                        id=trip_data['id'],
                        vehicleId=trip_data['vehicleId'],
                        driverId=trip_data.get('driverId'),
                        startTime=datetime.strptime(trip_data['startTime'], '%Y-%m-%d %H:%M:%S'),
                        endTime=datetime.strptime(trip_data['endTime'], '%Y-%m-%d %H:%M:%S'),
                        fullLoad=trip_data['fullLoad'],
                        tasks=trip_tasks
                    )
                    vehicle_trips.append(trip)
        
        vehicle = Vehicle(
            id=vehicle_data['id'],
            plateNumber=vehicle_data['plateNumber'],
            driverId=vehicle_data.get('driverId'),
            trips=vehicle_trips
        )
        vehicles.append(vehicle)
    
    return vehicles

def get_containers() -> List[Container]:
    """获取所有容器"""
    containers = []
    for container_data in DB['containers']:
        container = Container(**container_data)
        containers.append(container)
    return containers

def get_container_by_number(ctn_number: str) -> Optional[Container]:
    """根据容器号获取容器信息"""
    for container_data in DB['containers']:
        if container_data['CTN NUMBER'] == ctn_number:
            return Container(**container_data)
    return None

def add_task(task_data: dict) -> Task:
    """添加任务"""
    task = Task(**task_data)
    DB['tasks'].append(task.dict())
    
    # 更新行程数据
    for trip_data in DB['trips']:
        if trip_data['id'] == task_data['tripId']:
            if 'tasks' not in trip_data:
                trip_data['tasks'] = []
            trip_data['tasks'].append(task.dict())
            break
    
    return task

def delete_task(task_id: str) -> bool:
    """删除任务"""
    for i, task_data in enumerate(DB['tasks']):
        if task_data['id'] == task_id:
            DB['tasks'].pop(i)
            
            # 从行程数据中移除任务
            for trip_data in DB['trips']:
                if 'tasks' in trip_data:
                    trip_data['tasks'] = [t for t in trip_data['tasks'] if t['id'] != task_id]
            
            return True
    return False

def add_trip(trip_data: dict) -> Trip:
    """添加行程"""
    trip = Trip(**trip_data)
    trip_dict = trip.dict()
    trip_dict['tasks'] = []  # 初始化任务列表
    DB['trips'].append(trip_dict)
    
    # 更新车辆数据
    for vehicle_data in DB['vehicles']:
        if vehicle_data['id'] == trip_data['vehicleId']:
            vehicle_data['trips'].append(trip_dict)
            break
    
    return trip

def delete_trip(trip_id: str) -> bool:
    """删除行程"""
    # 删除相关任务
    DB['tasks'] = [task for task in DB['tasks'] if task['tripId'] != trip_id]
    
    # 删除行程
    for i, trip_data in enumerate(DB['trips']):
        if trip_data['id'] == trip_id:
            DB['trips'].pop(i)
            
            # 从车辆数据中移除
            for vehicle_data in DB['vehicles']:
                vehicle_data['trips'] = [
                    trip for trip in vehicle_data['trips'] 
                    if trip['id'] != trip_id
                ]
            return True
    return False

def update_trip_pm(trip_id: str, new_pm_id: str, new_start_time: datetime) -> bool:
    """更新行程车辆"""
    for trip_data in DB['trips']:
        if trip_data['id'] == trip_id:
            old_vehicle_id = trip_data['vehicleId']
            
            # 计算新的结束时间（保持时长不变）
            old_start = datetime.strptime(trip_data['startTime'], '%Y-%m-%d %H:%M:%S')
            old_end = datetime.strptime(trip_data['endTime'], '%Y-%m-%d %H:%M:%S')
            duration = old_end - old_start
            new_end_time = new_start_time + duration
            
            # 更新行程数据
            trip_data['vehicleId'] = new_pm_id
            trip_data['startTime'] = new_start_time.strftime('%Y-%m-%d %H:%M:%S')
            trip_data['endTime'] = new_end_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # 更新车辆关系
            # 从旧车辆移除
            for vehicle_data in DB['vehicles']:
                if vehicle_data['id'] == old_vehicle_id:
                    vehicle_data['trips'] = [
                        trip for trip in vehicle_data['trips'] 
                        if trip['id'] != trip_id
                    ]
            
            # 添加到新车辆
            for vehicle_data in DB['vehicles']:
                if vehicle_data['id'] == new_pm_id:
                    vehicle_data['trips'].append(trip_data)
            
            return True
    return False

def update_trip_time(trip_id: str, new_start: datetime, new_end: datetime) -> bool:
    """更新行程时间"""
    for trip_data in DB['trips']:
        if trip_data['id'] == trip_id:
            trip_data['startTime'] = new_start.strftime('%Y-%m-%d %H:%M:%S')
            trip_data['endTime'] = new_end.strftime('%Y-%m-%d %H:%M:%S')
            return True
    return False

# 初始化示例数据
init_sample_data()
