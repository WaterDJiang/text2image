from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app

# 配置CORS - 针对前后端分离的配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # 本地前端开发环境
        "https://image2text-web.vercel.app",  # 前端部署地址
        "https://image2text-web-waterdjiang.vercel.app",  # 前端部署地址
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导出 FastAPI 应用实例供 Vercel 使用
app = app 