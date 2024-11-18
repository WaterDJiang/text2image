from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app

# 配置CORS
origins = ["*"]  # 在生产环境中应该替换为实际域名

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导出 FastAPI 应用实例供 Vercel 使用
app = app