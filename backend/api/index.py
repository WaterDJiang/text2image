from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在 Vercel 环境中,前后端在同一域名下
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导出 FastAPI 应用实例供 Vercel 使用
app = app