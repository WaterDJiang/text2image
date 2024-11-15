import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ImgBBService:
    def __init__(self):
        self.api_key = os.getenv('IMGBB_API_KEY')
        self.upload_url = "https://api.imgbb.com/1/upload"
        
        # 创建一个带有重试机制的会话
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def upload_image(self, image_data):
        try:
            payload = {
                "key": self.api_key,
                "image": image_data
            }
            
            logger.debug("正在尝试上传图片到ImgBB...")
            
            # 使用会话发送请求，禁用SSL验证
            response = self.session.post(
                self.upload_url, 
                data=payload,
                verify=False,
                timeout=30
            )
            
            logger.debug(f"ImgBB响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.debug(f"ImgBB完整响应: {result}")  # 添加完整响应日志
                
                # 获取直接图片URL
                if "data" in result and "url" in result["data"]:
                    image_url = result["data"]["url"]
                    logger.debug(f"获取到的图片URL: {image_url}")
                    return image_url
                else:
                    logger.error("ImgBB响应中未找到图片URL")
                    return None
            else:
                logger.error(f"上传失败: HTTP {response.status_code}")
                logger.error(f"响应内容: {response.text}")
                return None
                
        except requests.exceptions.SSLError as e:
            logger.error(f"SSL错误: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"请求错误: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"未预期的错误: {str(e)}")
            return None 