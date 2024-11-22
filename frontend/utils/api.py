import requests
import base64
from PIL import Image
import io
import streamlit as st
import json
import cairosvg  # 添加 cairosvg 用于转换 SVG

def generate_image(text, provider="DeepSeek", model="qwen2.5", temperature=0.7, max_tokens=500):
    """调用后端API生成图片"""
    try:
        # 从 Streamlit secrets 获取配置
        api_key = st.secrets["DEEPSEEK_API_KEY"]
        api_base = st.secrets["DEEPSEEK_API_BASE"]
        
        # 设置请求头
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        
        # 构建请求数据
        payload = {
            "text": text,
            "provider": provider,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # 调用后端API
        response = requests.post(
            "http://localhost:8000/generate",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # 如果返回的是SVG代码
            if 'image' in result and isinstance(result['image'], str) and '<svg' in result['image']:
                try:
                    # 将SVG转换为PNG格式的字节数据
                    png_data = cairosvg.svg2png(bytestring=result['image'].encode('utf-8'))
                    return png_data
                except Exception as e:
                    st.error(f"SVG转换失败: {str(e)}")
                    return None
            
            # 如果是其他格式的图片数据
            image_data = result.get('image', None)
            if image_data:
                if isinstance(image_data, str):
                    if image_data.startswith('data:image'):
                        # Base64格式的图片
                        return base64.b64decode(image_data.split(',')[1])
                    elif image_data.startswith(('http://', 'https://')):
                        # URL格式的图片
                        return image_data
                    else:
                        try:
                            # 尝试作为Base64解码
                            return base64.b64decode(image_data)
                        except:
                            st.error("无法解析的图片数据格式")
                            return None
                return image_data
            return None
        else:
            raise Exception(f"API请求失败: {response.status_code} - {response.text}")
            
    except Exception as e:
        raise Exception(f"生成图片失败: {str(e)}") 