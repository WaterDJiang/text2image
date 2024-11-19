from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv
from .services.imgbb_service import ImgBBService
from .services.coze_service import CozeService
from .services.deepseek_service import DeepseekService
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(title="AI图片处理服务")

# 在创建 FastAPI 应用后添加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型
class PoetryRequest(BaseModel):
    text: str
    model: str = "deepseek"

@app.get("/")
async def root():
    return {"message": "Welcome to Image2Text API"}

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
            logger.error("图片上传失败")
            raise HTTPException(status_code=400, detail="图片上传失败，请稍后重试")
        
        # 根据选择的模型调用相应的服务
        service = DeepseekService() if model == "deepseek" else CozeService()
        result = await service.process_image(image_url, workflow_type)
        
        if not result:
            raise HTTPException(status_code=400, detail="图片处理失败")
        
        return result
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-poetry")
async def process_poetry(request: PoetryRequest):
    """处理诗歌生成请求"""
    try:
        logger.info(f"Processing poetry with text: {request.text}")
        
        # 根据选择的模型调用相应的服务
        service = DeepseekService() if request.model == "deepseek" else CozeService()
        result = await service.process_poetry(request.text)
        
        if not result:
            raise HTTPException(status_code=400, detail="诗歌生成失败")
        
        return result
        
    except Exception as e:
        logger.error(f"Poetry processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 全局错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )