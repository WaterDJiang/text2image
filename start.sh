#!/bin/bash

# 显示启动信息
echo "正在启动 AI 图片处理服务..."

# 检查必要的命令是否存在
command -v python3 >/dev/null 2>&1 || { echo "错误: 需要 python3 但未安装"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "错误: 需要 node 但未安装"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "错误: 需要 npm 但未安装"; exit 1; }

# 启动后端服务
echo "启动后端服务..."
cd backend

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
python -m pip install --upgrade pip

# 安装后端依赖
echo "安装后端依赖..."
pip install -r requirements.txt --no-cache-dir

# 启动后端服务
echo "启动后端服务..."
python run.py &
BACKEND_PID=$!

# 等待后端服务启动
echo "等待后端服务启动..."
sleep 5

# 检查后端服务是否成功启动
curl -s http://localhost:8000/api/health > /dev/null
if [ $? -ne 0 ]; then
    echo "错误: 后端服务启动失败"
    kill $BACKEND_PID
    exit 1
fi

echo "后端服务启动成功！"

# 返回上级目录
cd ..

# 启动前端服务
echo "启动前端服务..."
cd frontend

# 安装前端依赖
echo "安装前端依赖..."
npm install

# 启动前端开发服务器
npm run dev &
FRONTEND_PID=$!

echo "服务启动完成！"
echo "前端服务地址: http://localhost:5173"
echo "后端服务地址: http://localhost:8000"

# 等待用户按 Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 