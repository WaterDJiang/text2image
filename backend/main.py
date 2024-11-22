from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import sys
from backend.services.app_service import AppService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()
app_service = AppService()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    text: str
    provider: str = "Ollama"
    model: str = "qwen2.5"
    temperature: float = 0.7
    max_tokens: int = 500

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return await app_service.check_services()

@app.post("/generate")
async def generate_image(request: PromptRequest):
    """生成图片接口"""
    try:
        logger.info(f"收到生成请求: {request.text[:50]}...")
        return await app_service.generate_response(request.dict())
    except Exception as e:
        logger.error(f"处理请求时发生错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """启动事件"""
    logger.info("后端服务启动中...")
    health = await app_service.check_services()
    if not health["ollama"]:
        logger.warning("Ollama服务未就绪")
    logger.info("后端服务启动完成") 