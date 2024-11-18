from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app

# 配置CORS
origins = [
    "http://localhost:5173",  # 本地前端开发服务器
    "http://localhost:8000",  # 本地后端服务器
    "https://image2text.vercel.app",  # Vercel 部署域名
    "https://image2text-git-main-your-username.vercel.app",  # Vercel 预览域名
    "https://image2text-*.vercel.app"  # Vercel 预览域名通配符
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导出 FastAPI 应用实例供 Vercel 使用
app = app