from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# 添加后端目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, backend_dir)

from backend.app.main import app

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建 handler
handler = Mangum(app, lifespan="off")