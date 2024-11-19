#!/bin/bash

echo "正在启动 AI 图片处理服务..."

# 检查环境变量文件
if [ ! -f backend/.env ]; then
    echo "错误: 未找到环境变量文件 backend/.env"
    exit 1
fi

# 检查操作系统并安装必要的系统依赖
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "错误: 未找到 Homebrew，请先安装 Homebrew"
        exit 1
    fi
    
    echo "安装系统依赖..."
    brew install python3 node libjpeg libpng
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3-dev python3-pip nodejs npm libjpeg-dev libpng-dev
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-devel python3-pip nodejs npm libjpeg-turbo-devel libpng-devel
    fi
fi

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
if ! npm install; then
    echo "错误: 前端依赖安装失败"
    exit 1
fi

# 启动前端开发服务器
echo "启动前端服务..."
npm run dev &
FRONTEND_PID=$!

# 返回根目录
cd ..

# 创建并激活 Python 虚拟环境
echo "配置 Python 环境..."
cd backend
if [ -d "venv" ]; then
    echo "删除旧的虚拟环境..."
    rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate

# 升级基础工具
echo "升级基础工具..."
python3 -m pip install --upgrade pip setuptools wheel

# 安装后端依赖
echo "安装后端依赖..."
if ! pip install -r ../requirements.txt; then
    echo "错误: 后端依赖安装失败"
    exit 1
fi

# 检查并停止已存在的后端服务
BACKEND_PORT=8000
if lsof -i :$BACKEND_PORT > /dev/null; then
    echo "端口 $BACKEND_PORT 已被占用，正在停止..."
    kill $(lsof -t -i :$BACKEND_PORT)
    sleep 2
fi

# 启动后端服务
echo "启动后端服务..."
if ! uvicorn api.index:app --reload --port 8000 &; then
    echo "错误: 后端服务启动失败"
    exit 1
fi
BACKEND_PID=$!

# 保存进程 ID
echo $FRONTEND_PID > ../.frontend.pid
echo $BACKEND_PID > ../.backend.pid

echo "服务启动完成！"
echo "前端服务地址: http://localhost:5173"
echo "后端服务地址: http://localhost:8000"

# 等待服务启动
sleep 2

# 检查服务是否正常运行
if ! curl -s http://localhost:5173 > /dev/null; then
    echo "警告: 前端服务可能未正常启动"
fi

if ! curl -s http://localhost:8000/api/test > /dev/null; then
    echo "警告: 后端服务可能未正常启动"
fi