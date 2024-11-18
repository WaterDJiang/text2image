from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app

# 配置CORS
origins = [
    "http://localhost:5173",  # 本地前端开发服务器
    "http://localhost:8000",  # 本地后端服务器
    "https://image2text.vercel.app"  # Vercel 部署域名
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保所有路由都以 /api 开头
@app.get("/")
async def root():
    return {"message": "API is running"}

# 导出 FastAPI 应用实例供 Vercel 使用
app = app