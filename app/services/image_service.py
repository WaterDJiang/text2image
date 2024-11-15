import requests
from werkzeug.utils import secure_filename
import logging

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self, imgbb_api_key):
        self.imgbb_api_key = imgbb_api_key
        
    def upload_to_imgbb(self, image_file, max_retries=3):
        for attempt in range(max_retries):
            try:
                imgbb_url = f"https://api.imgbb.com/1/upload?key={self.imgbb_api_key}"
                files = {
                    'image': (
                        secure_filename(image_file.filename),
                        image_file.read(),
                        image_file.content_type
                    )
                }
                response = requests.post(imgbb_url, files=files, timeout=10)
                
                if response.status_code == 200:
                    return response.json()['data']['url']
                
                logger.warning(f"Upload attempt {attempt + 1} failed: {response.status_code}")
                
            except Exception as e:
                logger.error(f"Upload attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                
        raise Exception("Max retries exceeded") 