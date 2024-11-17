from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app

# 配置CORS - 针对前后端分离的配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，因为我们在 vercel.json 中已经配置了 CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导出 FastAPI 应用实例供 Vercel 使用
app = app 