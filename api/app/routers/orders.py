# 订单相关API路由
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models import ApiResponse, Container, TaskCreate
from app.database import get_containers, get_container_by_number
from app.utils import create_task_from_container

router = APIRouter()

@router.get("/containers")
async def get_containers_list(
    search: Optional[str] = Query(None, description="搜索关键词"),
    logisticsStatus: Optional[str] = Query(None, description="物流状态"),
    deliverType: Optional[str] = Query(None, description="交付类型"),
    terminal: Optional[str] = Query(None, description="码头")
):
    """获取容器列表"""
    try:
        containers = get_containers()
        
        # 应用筛选条件
        if search:
            containers = [
                c for c in containers 
                if search.lower() in c.ctnNumber.lower() or 
                   search.lower() in c.fullClientName.lower()
            ]
        
        if logisticsStatus:
            containers = [c for c in containers if c.logisticsStatus == logisticsStatus]
        
        if deliverType:
            containers = [c for c in containers if c.deliverType == deliverType]
        
        if terminal:
            containers = [c for c in containers if c.terminal == terminal]
        
        return ApiResponse(
            code=0,
            message="ok",
            data=[container.dict() for container in containers]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取容器列表失败: {str(e)}")

@router.get("/container/{ctn_number}")
async def get_container_detail(ctn_number: str):
    """获取容器详情"""
    try:
        container = get_container_by_number(ctn_number)
        
        if not container:
            return ApiResponse(code=404, message="容器不存在", data=None)
        
        return ApiResponse(code=0, message="ok", data=container.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取容器详情失败: {str(e)}")

@router.post("/plan-to-task")
async def plan_to_task(task_create: TaskCreate):
    """容器转换为任务"""
    try:
        # 查找容器
        container = get_container_by_number(task_create.containerNo)
        if not container:
            return ApiResponse(code=404, message="容器不存在", data=None)
        
        # 创建任务数据
        task_data = create_task_from_container(
            container=container,
            task_type=task_create.taskType,
            trip_id=task_create.tripId,
            vehicle_id=task_create.vehicleId,
            plan_start=task_create.planStart,
            plan_end=task_create.planEnd
        )
        
        # 如果是为现有行程添加任务，需要验证行程状态
        if task_create.tripId:
            from app.database import DB
            
            trip = None
            for t in DB['trips']:
                if t['id'] == task_create.tripId:
                    trip = t
                    break
            
            if not trip:
                return ApiResponse(code=40002, message="行程不存在", data=None)
            
            if trip['fullLoad'] == 'Y':
                return ApiResponse(code=40002, message="行程已满载，无法添加任务", data=None)
            
            # 检查任务数量限制
            existing_tasks = [task for task in DB['tasks'] if task['tripId'] == task_create.tripId]
            if len(existing_tasks) >= 2:
                return ApiResponse(code=40002, message="行程任务数量已达上限", data=None)
        
        return ApiResponse(code=0, message="ok", data=task_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"容器转任务失败: {str(e)}")
