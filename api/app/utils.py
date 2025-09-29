# 工具函数
from datetime import datetime, timedelta
from typing import Dict, Any
from app.models import Container, TaskType

def pickup_address(container: Container) -> str:
    """获取取货地址"""
    status = container.logisticsStatus
    
    if status == '新订单':
        return container.terminal
    elif status == 'Yard(F)':
        return f"{container.fullClientName} - Ready to Deliver"
    elif status == 'Client':
        return container.fullDeliverAddress
    elif status == 'Yard(E)':
        return f"{container.fullClientName} - Ready to De-hire"
    elif status == 'Empty Park':
        return container.emptyPark
    else:
        return container.terminal

def delivery_address(task_type: TaskType, container: Container) -> str:
    """获取送货地址"""
    address_map = {
        'Yard(F)': f"{container.fullClientName} - Ready to Deliver",
        'Client': container.fullDeliverAddress,
        'Yard(E)': f"{container.fullClientName} - Ready to De-hire",
        'Empty Park': container.emptyPark,
        'Drving': 'In Transit',
        'Lifting': 'Lifting Location',
        'Waiting': 'Waiting Area',
        'Other': 'Other Location',
    }
    
    return address_map.get(task_type, container.fullDeliverAddress)

def create_task_from_container(container: Container, task_type: TaskType, 
                              trip_id: str = None, vehicle_id: str = None,
                              plan_start: datetime = None, plan_end: datetime = None) -> Dict[str, Any]:
    """从容器创建任务"""
    import uuid
    
    # 默认时间：当前小时起60分钟
    if not plan_start:
        now = datetime.now()
        plan_start = now.replace(minute=0, second=0, microsecond=0)
    
    if not plan_end:
        plan_end = plan_start + timedelta(minutes=60)
    
    task = {
        'id': str(uuid.uuid4()),
        'tripId': trip_id or '',
        'containerNo': container.ctnNumber,
        'taskType': task_type,
        'planStart': plan_start.strftime('%Y-%m-%d %H:%M:%S'),
        'planEnd': plan_end.strftime('%Y-%m-%d %H:%M:%S'),
        'startAddress': pickup_address(container),
        'endAddress': delivery_address(task_type, container),
        'status': 'pending',
        'containerWeight': container.ctnWeight,
        'containerType': container.ctnType
    }
    
    return task
