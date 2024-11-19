from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import logging
import os
from .services.imgbb_service import ImgBBService
from .services.coze_service import CozeService
from .services.deepseek_service import DeepseekService
from pydantic import BaseModel

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 请求模型
class PoetryRequest(BaseModel):
    text: str
    model: str = "deepseek"

# 创建 FastAPI 应用
app = FastAPI(title="AI图片处理服务")

@app.get("/api/test")
async def test_route():
    """测试路由"""
    try:
        return {
            "message": "API is working",
            "status": "ok"
        }
    except Exception as e:
        logger.error(f"Test route error: {str(e)}")
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
        image_url = await imgbb_service.upload_image(contents)
        
        if not image_url:
            raise HTTPException(status_code=400, detail="图片上传失败")
        
        # 根据选择的模型调用相应的服务
        service = DeepseekService() if model == "deepseek" else CozeService()
        result = await service.process_image(image_url, workflow_type)
        
        if not result:
            raise HTTPException(status_code=400, detail="图片处理失败")
        
        return result
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-poetry")
async def process_poetry(request: PoetryRequest):
    """处理诗意文本API"""
    try:
        service = DeepseekService() if request.model == "deepseek" else CozeService()
        result = await service.process_poetry(request.text)
        
        if not result:
            raise HTTPException(status_code=400, detail="生成失败")
        
        return result
        
    except Exception as e:
        logger.error(f"处理诗意文本时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 全局错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )