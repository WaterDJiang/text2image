import requests
import os
import logging
import base64
from ..config import settings

logger = logging.getLogger(__name__)

class ImgBBService:
    def __init__(self):
        self.api_key = settings.IMGBB_API_KEY
        self.upload_url = "https://api.imgbb.com/1/upload"
    
    def upload_image(self, image_data):
        try:
            # 将二进制数据转换为base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            payload = {
                "key": self.api_key,
                "image": base64_image
            }
            
            logger.debug("正在上传图片到ImgBB...")
            response = requests.post(self.upload_url, data=payload)
            
            if response.status_code == 200:
                result = response.json()
                logger.debug(f"ImgBB响应: {result}")
                
                if result.get('data', {}).get('url'):
                    return result['data']['url']
                else:
                    logger.error(f"ImgBB返回数据中没有URL: {result}")
            
            logger.error(f"ImgBB上传失败: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"上传图片时发生错误: {str(e)}")
            return None 