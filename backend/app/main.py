from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
import logging
from .services.imgbb_service import ImgBBService
from .services.coze_service import CozeService
from .services.image_service import ImageService
from .config import settings
from pydantic import BaseModel

# 配置日志记录器
logger = logging.getLogger(__name__)

# 创建FastAPI应用实例
app = FastAPI(title="AI图片处理服务")

# 配置跨域资源共享(CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # 本地开发环境
        "https://image2text-web.vercel.app",  # Vercel 前端部署地址
        "https://image2text-web-waterdjiang.vercel.app",  # 实际的 Vercel 前端部署地址
        "https://image2text-web-backend.vercel.app"  # 后端地址
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加请求体模型
class PoetryRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    """根路径处理程序"""
    return {"message": "Welcome to AI Image Processing API"}

@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

@app.post("/api/process-image")
async def process_image(
    file: UploadFile = File(...),
    workflow_type: str = Form("mood")
):
    """处理图片API"""
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="只支持图片文件")
        
        contents = await file.read()
        
        imgbb_service = ImgBBService()
        image_url = imgbb_service.upload_image(contents)
        
        if not image_url:
            raise HTTPException(status_code=400, detail="图片上传失败")
        
        logger.debug(f"成功获取到图片URL: {image_url}")
        
        coze_service = CozeService()
        result = coze_service.process_image(image_url, workflow_type)
        
        if not result:
            raise HTTPException(status_code=400, detail="图片处理失败")
        
        return result
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"处理图片时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-poetry")
async def process_poetry(request: PoetryRequest):
    """处理诗意文本API"""
    try:
        coze_service = CozeService()
        result = coze_service.process_poetry(request.text)
        
        if not result:
            raise HTTPException(status_code=400, detail="生成失败")
        
        return result
        
    except Exception as e:
        logger.error(f"处理诗意文本时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# 添加一个测试路由
@app.get("/api/test")
async def test_route():
    return {"message": "API is working"} 