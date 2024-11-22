import os
import requests
import streamlit as st
from typing import Optional, Dict, Any
import json
from openai import AsyncOpenAI

class APIService:
    """API服务适配器，支持本地FastAPI和云端模式"""
    
    def __init__(self):
        self.is_local = self._is_local_env()
        if self.is_local:
            self.base_url = "http://localhost:8000"
        else:
            # Streamlit Cloud模式下直接使用DeepSeek API
            self.client = AsyncOpenAI(
                api_key=st.secrets["DEEPSEEK_API_KEY"],
                base_url=st.secrets["DEEPSEEK_API_BASE"]
            )
    
    def _is_local_env(self) -> bool:
        """检查是否为本地环境"""
        return os.environ.get("IS_LOCAL", "").lower() == "true"
    
    async def generate_image(self, text: str, params: Dict[str, Any]) -> Optional[bytes]:
        """生成图片的统一接口"""
        try:
            if self.is_local:
                # 本地模式：调用FastAPI后端
                response = requests.post(
                    f"{self.base_url}/generate",
                    json={
                        "text": text,
                        **params
                    }
                )
                if response.status_code == 200:
                    return response.json()
            else:
                # 云端模式：直接调用DeepSeek API
                response = await self.client.chat.completions.create(
                    model=params.get("model", "deepseek-chat"),
                    messages=[
                        {
                            "role": "system",
                            "content": st.secrets.get("SYSTEM_PROMPT", "")
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    temperature=params.get("temperature", 0.7),
                    max_tokens=params.get("max_tokens", 500)
                )
                return self._process_cloud_response(response)
                
        except Exception as e:
            st.error(f"生成失败: {str(e)}")
            return None
    
    def _process_cloud_response(self, response):
        """处理云端API响应"""
        content = response.choices[0].message.content
        
        # 提取评论和SVG
        comment = ""
        svg = ""
        
        if "【点评】" in content:
            comment = content.split("【点评】")[1].split("【SVG】")[0].strip()
        if "【SVG】" in content:
            svg = content.split("【SVG】")[1].strip()
            
        return {
            "comment": comment,
            "svg": svg
        }
    
    async def check_health(self) -> Dict[str, bool]:
        """检查服务健康状态"""
        if self.is_local:
            try:
                response = requests.get(f"{self.base_url}/health")
                return response.json() if response.status_code == 200 else {"status": "unhealthy"}
            except:
                return {"status": "unhealthy"}
        else:
            try:
                # 简单的API测试
                response = await self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5
                )
                return {"status": "healthy", "deepseek": True}
            except:
                return {"status": "unhealthy", "deepseek": False} 