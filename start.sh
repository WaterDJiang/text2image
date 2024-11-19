#!/bin/bash

# 启动后端服务
uvicorn backend.api.index:app --reload --host 0.0.0.0 --port 8000 &

# 启动前端服务
cd frontend && npm run dev &

# 等待所有后台进程
wait