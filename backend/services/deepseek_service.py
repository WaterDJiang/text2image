from openai import AsyncOpenAI
import logging
import json
from backend.config.prompts import SYSTEM_PROMPT
from backend.config.settings import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE

logger = logging.getLogger(__name__)

class DeepseekService:
    def __init__(self):
        """初始化DeepSeek服务"""
        logger.info("正在初始化 DeepSeek 服务...")
        if not DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")
            
        logger.info(f"使用 API Base URL: {DEEPSEEK_API_BASE}")
        
        try:
            self.client = AsyncOpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_API_BASE
            )
            logger.info("DeepSeek 服务初始化成功")
        except Exception as e:
            logger.error(f"DeepSeek 服务初始化失败: {str(e)}")
            raise
    
    async def check_health(self):
        """检查服务健康状态"""
        try:
            # 尝试进行一个简单的API调用来检查服务是否可用
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"DeepSeek服务健康检查失败: {str(e)}")
            return False
    
    async def generate(self, text, model="deepseek-chat", temperature=0.7, max_tokens=500):
        """生成内容"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            
            content = response.choices[0].message.content
            
            # 提取点评和SVG内容
            comment = ""
            svg = ""
            
            if "【点评】" in content:
                comment = content.split("【点评】")[1].split("【SVG】")[0].strip()
            if "【SVG】" in content:
                svg = content.split("【SVG】")[1].strip()
                
            logger.info(f"生成的点评: {comment}")
            logger.debug(f"生成的SVG: {svg[:100]}...")
            
            return comment, svg
            
        except Exception as e:
            logger.error(f"DeepSeek生成失败: {str(e)}")
            raise 