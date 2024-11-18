#!/bin/bash

echo "正在停止服务..."

# 停止前端服务
if [ -f .frontend.pid ]; then
    kill $(cat .frontend.pid)
    rm .frontend.pid
fi

# 停止后端服务
if [ -f .backend.pid ]; then
    kill $(cat .backend.pid)
    rm .backend.pid
fi

echo "服务已停止" 