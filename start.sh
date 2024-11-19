#!/bin/bash

# 加载环境变量
if [ -f .env ]; then
    echo "Loading environment variables from .env file"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Warning: .env file not found"
fi

# 检查必要的环境变量
required_vars=(
    "COZE_API_KEY"
    "DEEPSEEK_API_KEY"
    "IMGBB_API_KEY"
    "WORKFLOW_ID_MOOD"
    "WORKFLOW_ID_SARCASTIC"
    "WORKFLOW_ID_POETRY"
    "WORKFLOW_ID_STORY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not set"
        exit 1
    fi
done

if [[ ! "$COZE_API_KEY" =~ ^pat_.+ ]]; then
    echo "Error: COZE_API_KEY must start with 'pat_'"
    exit 1
fi

# 设置环境变量
export ENV=${1:-development}

echo "Starting backend service..."
# 启动后端服务
if [ "$ENV" = "production" ]; then
    echo "Running in production mode"
    uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
else
    echo "Running in development mode"
    uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000 &
fi
BACKEND_PID=$!
echo $BACKEND_PID > .backend.pid

# 等待后端启动
sleep 2

echo "Starting frontend service..."
# 启动前端服务
cd frontend
VITE_API_BASE_URL=http://localhost:8000/api npm run dev -- --host &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../.frontend.pid
cd ..

echo "Services started:"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

# 等待所有进程完成
wait