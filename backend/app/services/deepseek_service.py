import openai
import logging
import json
import os
from dotenv import load_dotenv
import traceback
from ..config.prompts import SYSTEM_PROMPTS, POETRY_PROMPT
import base64
from PIL import Image
import requests
from io import BytesIO
from .image_service import ImageService  # 确保正确导入

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

class DeepseekService:
    def __init__(self):
        """初始化DeepseekService"""
        logger.info("正在初始化 DeepSeek 服务...")
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")
            
        try:
            openai.api_key = self.api_key
            openai.api_base = os.getenv('DEEPSEEK_API_BASE', "https://api.deepseek.com/v1")
            logger.info("DeepSeek 服务初始化成功")
        except Exception as e:
            logger.error(f"DeepSeek 服务初始化失败: {str(e)}")
            raise
        
        self.image_service = ImageService()  # 在初始化时创建 ImageService 实例
        
    async def _get_image_description(self, image_url: str, workflow_type: str) -> str:
        """获取图片描述"""
        try:
            # 使用对应工作流类型的 prompt
            system_prompt = SYSTEM_PROMPTS.get(workflow_type, SYSTEM_PROMPTS['mood'])
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"请基于这张图片进行创作: {image_url}"
                }
            ]
            
            logger.debug(f"API请求参数: {json.dumps(messages, ensure_ascii=False)}")
            
            response = await openai.ChatCompletion.acreate(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                stream=False
            )
            
            description = response.choices[0].message.content
            logger.info("成功获取图片描述")
            return description
            
        except Exception as e:
            logger.error(f"获取图片描述失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise Exception(f"获取图片描述失败: {str(e)}")
    
    async def process_image(self, image_url: str, workflow_type: str = "mood") -> dict:
        """处理图片"""
        try:
            # 获取AI生成的描述文本
            output_text = await self._get_image_description(image_url, workflow_type)
            logger.info(f"生成的描述文本: {output_text}")
            
            # 调用图片服务生成明信片样式的图片
            try:
                image_service = ImageService()
                postcard_image = await image_service.create_postcard(
                    image_url=image_url,
                    text=output_text
                )
                if not postcard_image:
                    raise Exception("生成明信片图片失败: 返回为空")
                logger.info("成功生成带文字的明信片图片")
            except Exception as e:
                logger.error(f"生成明信片样式图片失败: {str(e)}")
                raise Exception(f"生成明信片样式图片失败: {str(e)}")
            
            return {
                "text": output_text,
                "postcard_image": postcard_image
            }
            
        except Exception as e:
            logger.error(f"图片处理失败: {str(e)}")
            raise Exception(f"图片处理失败: {str(e)}")
    
    async def process_poetry(self, text):
        try:
            logger.info("开始处理诗意文本...")
            
            messages = [
                {"role": "system", "content": POETRY_PROMPT},
                {"role": "user", "content": f"请为这段文字提供诗意点评和配图：{text}"}
            ]
            
            response = await openai.ChatCompletion.acreate(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                stream=False
            )
            
            content = response.choices[0].message.content
            
            comment = ""
            svg = ""
            
            if "【点评】" in content:
                comment = content.split("【点评】")[1].split("【SVG】")[0].strip()
            if "【SVG】" in content:
                svg = content.split("【SVG】")[1].strip()
                
            logger.info(f"生成的点评: {comment}")
            logger.debug(f"生成的SVG: {svg}")
            
            return {
                'comment': comment,
                'svg': svg
            }
                
        except Exception as e:
            logger.error(f"处理诗意文本时发生错误: {str(e)}", exc_info=True)
            return None