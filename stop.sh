#!/bin/bash

echo "Stopping services..."

# 停止前端服务
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
        kill $FRONTEND_PID
        rm .frontend.pid
        echo "Frontend service stopped"
    else
        echo "Frontend service not running"
    fi
else
    echo "Frontend service not running"
fi

# 停止后端服务
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
        kill $BACKEND_PID
        rm .backend.pid
        echo "Backend service stopped"
    else
        echo "Backend service not running"
    fi
else
    echo "Backend service not running"
fi

# 清理虚拟环境（可选）
# deactivate 2>/dev/null || true

echo -e "\nAll services stopped" 