#!/bin/bash

# 激活虚拟环境
if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ] || [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    source venv/Scripts/activate
fi

# 检查环境变量
if [ ! -f .env ]; then
    echo "错误: 未找到.env文件，请先运行setup.sh"
    exit 1
fi

# 检查Ollama服务
echo "检查Ollama服务..."
curl -s http://localhost:11434/api/version || {
    echo "错误: 无法连接到Ollama服务，请确保Ollama已启动"
    exit 1
}

# 设置 PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 启动后端服务
echo "启动后端服务..."
cd backend
python -m uvicorn main:app --reload --port 8000 --log-level info &
BACKEND_PID=$!

# 等待后端服务启动
echo "等待后端服务启动..."
max_attempts=30
attempt=0
while ! curl -s http://localhost:8000/health > /dev/null && [ $attempt -lt $max_attempts ]; do
    sleep 1
    attempt=$((attempt + 1))
    echo "等待后端服务启动中... ($attempt/$max_attempts)"
done

if [ $attempt -eq $max_attempts ]; then
    echo "错误: 后端服务启动超时"
    kill $BACKEND_PID
    exit 1
fi

echo "后端服务已启动！"

# 启动前端服务
echo "启动前端服务..."
cd ../frontend
PYTHONPATH=$PYTHONPATH:$(pwd)/.. streamlit run app.py

# 清理进程
trap 'kill $BACKEND_PID' EXIT