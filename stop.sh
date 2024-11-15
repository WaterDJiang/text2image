#!/bin/bash

echo "正在停止服务..."

# 查找并终止Python进程
pkill -f "python run.py"

# 查找并终止Node.js进程
pkill -f "npm run dev"

echo "服务已停止" 