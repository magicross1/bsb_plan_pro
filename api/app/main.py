# FastAPI主应用
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import gantt, orders

app = FastAPI(
    title="BSB调度甘特系统API",
    description="BSB调度甘特系统的后端API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # 前端开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(gantt.router, prefix="/api/gantt", tags=["gantt"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"code": 0, "message": "ok", "data": {"status": "healthy"}}

@app.get("/")
async def root():
    """根路径"""
    return {"message": "BSB调度甘特系统API服务运行中"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
