import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)

class ImgBBService:
    def __init__(self):
        self.api_key = os.getenv('IMGBB_API_KEY')
        self.upload_url = "https://api.imgbb.com/1/upload"
    
    async def upload_image(self, image_data: bytes) -> Optional[str]:
        """异步上传图片到ImgBB"""
        try:
            files = {'image': image_data}
            params = {'key': self.api_key}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.upload_url,
                    params=params,
                    files=files
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get('success'):
                    return result['data']['url']
                return None
                
        except Exception as e:
            logger.error(f"ImgBB upload error: {str(e)}")
            return None 