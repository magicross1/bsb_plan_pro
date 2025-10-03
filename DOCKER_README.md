# BSB调度甘特系统 - Docker 部署指南

## 🚀 一键启动

### 前提条件
- 安装 [Docker](https://www.docker.com/get-started)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/)

### 快速启动
```bash
# 1. 克隆项目
git clone <your-repo-url>
cd bsb_plan_pro

# 2. 一键启动所有服务
docker-compose up -d

# 3. 访问应用
# 前端: http://localhost
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

## 📋 服务说明

### 前端服务 (端口 80)
- **访问地址**: http://localhost
- **技术栈**: Vue 3 + Vite + Element Plus
- **容器名**: bsb-frontend

### 后端服务 (端口 8000)
- **访问地址**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **技术栈**: FastAPI + Python 3.11
- **容器名**: bsb-backend

## 🛠️ 常用命令

### 启动服务
```bash
# 后台启动
docker-compose up -d

# 前台启动（查看日志）
docker-compose up

# 重新构建并启动
docker-compose up --build
```

### 停止服务
```bash
# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs frontend
docker-compose logs backend

# 实时查看日志
docker-compose logs -f
```

### 进入容器
```bash
# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh
```

### 重启服务
```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

## 🔧 开发模式

### 热重载开发
```bash
# 启动开发环境（支持热重载）
docker-compose -f docker-compose.dev.yml up
```

### 单独运行服务
```bash
# 只启动后端
docker-compose up backend

# 只启动前端
docker-compose up frontend
```

## 📊 健康检查

系统内置健康检查，确保服务正常运行：

```bash
# 检查服务状态
docker-compose ps

# 查看健康状态
docker inspect bsb-backend --format='{{.State.Health.Status}}'
docker inspect bsb-frontend --format='{{.State.Health.Status}}'
```

## 🐛 故障排除

### 端口冲突
如果端口被占用，可以修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8080:80"  # 前端改为 8080
  - "8001:8000"  # 后端改为 8001
```

### 权限问题
```bash
# 给脚本执行权限
chmod +x scripts/*.sh
```

### 清理环境
```bash
# 清理所有容器和镜像
docker-compose down --rmi all --volumes --remove-orphans

# 清理 Docker 系统
docker system prune -a
```

## 📁 项目结构
```
bsb_plan_pro/
├── api/                    # 后端代码
├── src/                    # 前端代码
├── docker-compose.yml      # Docker Compose 配置
├── Dockerfile.frontend     # 前端 Dockerfile
├── Dockerfile.backend      # 后端 Dockerfile
├── nginx.conf             # Nginx 配置
├── .dockerignore          # Docker 忽略文件
└── DOCKER_README.md       # 本文档
```

## 🌟 特性

- ✅ **开箱即用**: 无需安装 Node.js、Python 等环境
- ✅ **一键部署**: 单条命令启动整个系统
- ✅ **自动代理**: Nginx 自动代理 API 请求
- ✅ **健康检查**: 自动监控服务状态
- ✅ **热重载**: 开发模式支持代码热更新
- ✅ **生产就绪**: 优化的生产环境配置

## 📞 支持

如果遇到问题，请检查：
1. Docker 和 Docker Compose 是否正确安装
2. 端口是否被其他服务占用
3. 查看服务日志：`docker-compose logs`

---

**享受使用 BSB调度甘特系统！** 🎉
