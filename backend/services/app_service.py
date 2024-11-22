import logging
from .ollama_service import OllamaService
from .deepseek_service import DeepseekService
from .image_service import ImageService
from io import BytesIO
import base64

logger = logging.getLogger(__name__)

class AppService:
    def __init__(self):
        self.ollama_service = OllamaService()
        self.deepseek_service = DeepseekService()
        self.image_service = ImageService()
    
    async def generate_response(self, request_data):
        """生成完整的响应，包括文本和图片"""
        try:
            # 解析请求参数
            text = request_data["text"]
            provider = request_data.get("provider", "Ollama")
            model = request_data.get("model", "qwen2.5")
            temperature = float(request_data.get("temperature", 0.7))
            max_tokens = int(request_data.get("max_tokens", 500))
            
            # 根据提供商选择服务
            if provider.lower() == "ollama":
                comment, svg = await self.ollama_service.generate(
                    text,
                    model=model
                )
            else:  # DeepSeek
                comment, svg = await self.deepseek_service.generate(
                    text,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            
            # 创建图片
            img = self.image_service.create_image_with_svg(comment, svg)
            
            # 转换为base64
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {"image": img_str}
            
        except Exception as e:
            logger.error(f"生成响应失败: {str(e)}")
            raise
    
    async def check_services(self):
        """检查所有服务是否正常"""
        ollama_health = await self.ollama_service.check_health()
        deepseek_health = await self.deepseek_service.check_health()
        
        return {
            "ollama": ollama_health,
            "deepseek": deepseek_health,
            "status": "healthy" if (ollama_health or deepseek_health) else "unhealthy"
        } 