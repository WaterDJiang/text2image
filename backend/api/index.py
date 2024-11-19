from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import sys
import os

# 添加正确的 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, backend_dir)

from backend.app.main import app

# 配置CORS（跨域资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源
    allow_credentials=True,   # 允许携带凭证
    allow_methods=["*"],      # 允许的HTTP方法
    allow_headers=["*"],      # 允许的请求头
)

# 创建 handler，用于处理 AWS Lambda/Vercel 环境
handler = Mangum(app, lifespan="off")