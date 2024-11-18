#!/bin/bash

echo "正在启动 AI 图片处理服务..."

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python，请先安装 Python"
    exit 1
fi

# 检查 Node.js 环境
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

# 安装前端依赖
echo "安装前端依赖..."
cd frontend
npm install

# 启动前端开发服务器
echo "启动前端服务..."
npm run dev &
FRONTEND_PID=$!

# 返回根目录
cd ..

# 创建并激活 Python 虚拟环境
echo "配置 Python 环境..."
cd backend
python3 -m venv venv
source venv/bin/activate

# 安装后端依赖
echo "安装后端依赖..."
pip install -r requirements.txt

# 启动后端服务
echo "启动后端服务..."
uvicorn api.index:app --reload --port 8000 &
BACKEND_PID=$!

# 保存进程 ID
echo $FRONTEND_PID > ../.frontend.pid
echo $BACKEND_PID > ../.backend.pid

echo "服务启动完成！"
echo "前端服务地址: http://localhost:5173"
echo "后端服务地址: http://localhost:8000"