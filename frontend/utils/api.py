import requests
import base64
from PIL import Image
import io
import streamlit as st

def generate_image(text, provider="DeepSeek"):
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
            "prompt": text,
            "n": 1,
            "size": "1024x1024"
        }
        
        response = requests.post(
            f"{api_base}/images/generations",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API请求失败: {response.status_code} - {response.text}")
            
    except Exception as e:
        raise Exception(f"生成图片失败: {str(e)}") 