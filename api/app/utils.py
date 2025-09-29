# 工具函数
from datetime import datetime, timedelta, date
from typing import Dict, Any, Optional
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

"""时间处理模块"""
def Str2Date(s: str) -> Optional[date]:
    """把字符串转成 date 对象"""
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S"]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s).date()
    except Exception:
        return None

def Str2DateTime(s: str) -> Optional[datetime]:
    """把字符串转成 datetime 对象"""
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

def Date2Str(d: date, fmt: str = "%Y-%m-%d") -> str:
    """把 date 转成字符串"""
    return d.strftime(fmt)

def DateTime2Str(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """把 datetime 转成字符串"""
    return dt.strftime(fmt)

def DateTime2Date(dt: datetime) -> date:
    """把 datetime 转成 date"""
    return dt.date()

def Date2DateTime(d: date) -> datetime:
    """把 date 转成 datetime (默认 00:00:00)"""
    return datetime.combine(d, datetime.min.time())