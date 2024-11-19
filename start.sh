#!/bin/bash

# 启动后端服务
echo "Starting backend service..."
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo $BACKEND_PID > ../.backend.pid
cd ..

# 启动前端服务
echo "Starting frontend service..."
cd frontend
VITE_API_BASE_URL=http://localhost:8000/api npx vite --host &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../.frontend.pid
cd ..

echo "Services started:"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

# 等待所有进程完成
wait