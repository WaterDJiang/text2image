import httpx
import logging
import json
import re
from backend.config.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        
    async def check_health(self):
        """检查Ollama服务是否可用"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/version")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama服务检查失败: {str(e)}")
            return False
    
    def process_response(self, response_text):
        """处理Ollama的流式响应，提取点评和SVG内容"""
        full_response = ""
        for line in response_text.splitlines():
            if not line.strip():
                continue
            try:
                response_json = json.loads(line)
                if "response" in response_json:
                    full_response += response_json["response"]
            except json.JSONDecodeError:
                continue
        
        # 提取点评和SVG内容
        comment = ""
        svg = ""
        
        # 使用正则表达式提取内容
        comment_match = re.search(r'【点评】\s*(.*?)\s*(?=【SVG】|$)', full_response, re.DOTALL)
        svg_match = re.search(r'【SVG】\s*(<svg.*?</svg>)', full_response, re.DOTALL)
        
        if comment_match:
            comment = comment_match.group(1).strip()
        if svg_match:
            svg = svg_match.group(1).strip()
        
        return comment, svg
    
    async def generate(self, text, model="qwen2.5", temperature=0.7, max_tokens=500):
        """生成点评和SVG"""
        try:
            # 组合系统prompt和用户输入
            full_prompt = f"{SYSTEM_PROMPT}\n\n用户输入：{text}"
            
            logger.info(f"正在调用Ollama API，使用模型: {model}...")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": full_prompt,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "stream": True
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"Ollama API调用失败: {response.status_code}")
                    raise Exception(f"Ollama API调用失败: {response.status_code}")
                
                # 处理响应
                comment, svg = self.process_response(response.content.decode('utf-8'))
                logger.info(f"提取的评论: {comment}")
                logger.info(f"提取的SVG: {svg[:100]}...")  # 只记录SVG的开头部分
                
                return comment, svg
                
        except Exception as e:
            logger.error(f"生成失败: {str(e)}")
            raise 