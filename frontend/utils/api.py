import requests
import base64
from PIL import Image
import io

def generate_image(text, provider, model, temperature, max_tokens):
    """调用后端API生成图片"""
    try:
        request_data = {
            "text": text,
            "provider": provider,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            "http://localhost:8000/generate",
            json=request_data,
            timeout=60
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if "image" in response_data:
                img_bytes = base64.b64decode(response_data["image"])
                return Image.open(io.BytesIO(img_bytes))
        
        raise Exception(f"API调用失败: {response.status_code}")
    except Exception as e:
        raise Exception(f"生成图片失败: {str(e)}") 