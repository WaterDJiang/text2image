from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
import logging
import os
from .services.imgbb_service import ImgBBService
from .services.coze_service import CozeService
from .services.image_service import ImageService
from .config import settings
from pydantic import BaseModel
from .services.deepseek_service import DeepseekService

# 配置详细的日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 定义请求模型 - 移到这里，在使用之前定义
class PoetryRequest(BaseModel):
    text: str
    model: str = "deepseek"

# 创建FastAPI应用实例
app = FastAPI(title="AI图片处理服务")

# 检查环境变量
@app.on_event("startup")
async def startup_event():
    required_vars = [
        'COZE_API_URL',
        'COZE_API_KEY',
        'IMGBB_API_KEY',
        'WORKFLOW_ID_MOOD',
        'WORKFLOW_ID_SARCASTIC',
        'WORKFLOW_ID_POETRY',
        'WORKFLOW_ID_STORY',
        'DEEPSEEK_API_KEY'
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        raise Exception(f"Missing required environment variables: {missing_vars}")

# 全局错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.get("/api/test")
async def test_route():
    """测试路由"""
    try:
        # 测试环境变量
        env_vars = {
            'COZE_API_URL': os.getenv('COZE_API_URL'),
            'IMGBB_API_KEY': os.getenv('IMGBB_API_KEY'),
            'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY'),
            'PYTHONPATH': os.getenv('PYTHONPATH')
        }
        logger.info(f"Environment variables: {env_vars}")
        
        # 测试服务实例化
        imgbb_service = ImgBBService()
        coze_service = CozeService()
        deepseek_service = DeepseekService()
        
        return {
            "message": "API is working",
            "env_check": "Environment variables loaded",
            "services_check": "Services initialized"
        }
    except Exception as e:
        logger.error(f"Test route error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-image")
async def process_image(
    file: UploadFile = File(...),
    workflow_type: str = Form("mood"),
    model: str = Form("deepseek")
):
    """处理图片API"""
    try:
        logger.info(f"Processing image with workflow: {workflow_type}, model: {model}")
        
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="只支持图片文件")
        
        contents = await file.read()
        
        imgbb_service = ImgBBService()
        image_url = imgbb_service.upload_image(contents)
        
        if not image_url:
            raise HTTPException(status_code=400, detail="图片上传失败")
        
        # 根据选择的模型调用相应的服务
        if model == "deepseek":
            service = DeepseekService()
        else:
            service = CozeService()
            
        result = service.process_image(image_url, workflow_type)
        
        if not result:
            raise HTTPException(status_code=400, detail="图片处理失败")
        
        return result
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-poetry")
async def process_poetry(request: PoetryRequest, model: str = "deepseek"):
    """处理诗意文本API"""
    try:
        # 根据选择的模型调用相应的服务
        if model == "deepseek":
            service = DeepseekService()
        else:
            service = CozeService()
            
        result = service.process_poetry(request.text)
        
        if not result:
            raise HTTPException(status_code=400, detail="生成失败")
        
        return result
        
    except Exception as e:
        logger.error(f"处理诗意文本时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 