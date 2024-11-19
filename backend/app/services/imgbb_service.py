import os
import logging
import httpx
import base64
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

class ImgBBService:
    def __init__(self):
        self.api_key = os.getenv('IMGBB_API_KEY')
        if not self.api_key:
            raise ValueError("IMGBB_API_KEY environment variable is not set")
        self.upload_url = "https://api.imgbb.com/1/upload"
        self.max_retries = 3
        self.timeout = 60.0  # 增加超时时间到60秒
    
    async def _try_upload(self, client: httpx.AsyncClient, data: dict) -> Optional[str]:
        """单次尝试上传"""
        response = await client.post(
            self.upload_url,
            data=data,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            logger.error(f"ImgBB API返回错误状态码: {response.status_code}")
            logger.error(f"错误响应: {response.text}")
            return None
        
        result = response.json()
        logger.debug(f"ImgBB响应: {result}")
        
        if result.get('success'):
            image_url = result['data']['url']
            logger.info(f"图片上传成功: {image_url}")
            return image_url
        else:
            logger.error(f"ImgBB上传失败: {result.get('error', {}).get('message', '未知错误')}")
            return None
    
    async def upload_image(self, image_data: bytes) -> Optional[str]:
        """异步上传图片到ImgBB，带重试机制"""
        try:
            # 转换图片数据为base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # 准备请求数据
            data = {
                'key': self.api_key,
                'image': image_base64
            }
            
            logger.info("开始上传图片到ImgBB...")
            
            async with httpx.AsyncClient() as client:
                for attempt in range(self.max_retries):
                    try:
                        if attempt > 0:
                            logger.info(f"第 {attempt + 1} 次重试上传...")
                            # 重试前等待一段时间
                            await asyncio.sleep(2 ** attempt)  # 指数退避
                            
                        result = await self._try_upload(client, data)
                        if result:
                            return result
                            
                    except httpx.TimeoutException:
                        logger.warning(f"第 {attempt + 1} 次上传超时")
                        if attempt == self.max_retries - 1:
                            logger.error("上传尝试次数已达上限")
                            return None
                        continue
                    except httpx.RequestError as e:
                        logger.error(f"请求错误: {str(e)}")
                        return None
                        
            logger.error("所有上传尝试均失败")
            return None
                
        except Exception as e:
            logger.error(f"ImgBB上传发生未知错误: {str(e)}")
            return None