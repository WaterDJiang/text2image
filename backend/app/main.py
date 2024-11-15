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
    allow_origins=["http://localhost:5173"],  # Vue开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加请求体模型
class PoetryRequest(BaseModel):
    text: str

@app.post("/api/process-image")
async def process_image(
    file: UploadFile = File(...),  # 上传的图片文件
    workflow_type: str = Form("mood")  # 工作流类型，默认为mood
):
    """
    处理图片API
    1. 接收上传的图片
    2. 上传到ImgBB获取URL
    3. 调用Coze API处理图片
    """
    try:
        # 验证文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="只支持图片文件")
        
        # 读取上传的文件内
        contents = await file.read()
        
        # 上传到ImgBB图床
        imgbb_service = ImgBBService()
        image_url = imgbb_service.upload_image(contents)
        
        if not image_url:
            raise HTTPException(status_code=400, detail="图片上传失败")
        
        logger.debug(f"成功获取到图片URL: {image_url}")
        
        # 调用Coze API处理图片
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

@app.post("/api/resize-image")
async def resize_image(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...)
):
    """
    调整图片大小API
    1. 接收图片和目标尺寸
    2. 调整图片大小
    3. 返回base64编码的结果
    """
    try:
        # 验证文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="只支持图片文件")
        
        # 读取图片
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # 调整大小
        image_service = ImageService()
        resized_image = image_service.resize_image(image, width, height)
        
        # 转换为base64
        buffered = io.BytesIO()
        resized_image.save(buffered, format=image.format or 'PNG')
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            "resized_image": f"data:image/{image.format.lower() if image.format else 'png'};base64,{img_str}"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"调整图片大小时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-poetry")
async def process_poetry(request: PoetryRequest):
    """
    处理诗意文本API
    1. 接收文本输入
    2. 调用Coze API生成诗意内容
    3. 返回评论和SVG图片
    """
    try:
        coze_service = CozeService()
        result = coze_service.process_poetry(request.text)
        
        if not result:
            raise HTTPException(status_code=400, detail="生成失败")
        
        return result
        
    except Exception as e:
        logger.error(f"处理诗意文本时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 可以添加健康检查端点
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"} 