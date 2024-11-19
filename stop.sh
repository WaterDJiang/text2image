#!/bin/bash

echo "Stopping services..."

# 停止前端服务
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        echo "Stopping frontend service (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID
        kill $(lsof -t -i:5173) 2>/dev/null # 关闭可能占用的 Vite 端口
    else
        echo "Frontend service not running"
    fi
    rm .frontend.pid
fi

# 停止后端服务
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
        echo "Stopping backend service (PID: $BACKEND_PID)"
        kill $BACKEND_PID
        kill $(lsof -t -i:8000) 2>/dev/null # 关闭可能占用的后端端口
    else
        echo "Backend service not running"
    fi
    rm .backend.pid
fi

# 清理可能残留的端口占用
for port in {5173..5180}; do
    pid=$(lsof -t -i:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "Cleaning up port $port (PID: $pid)"
        kill $pid 2>/dev/null
    fi
done

echo "All services stopped" 