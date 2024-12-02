from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import json
from urllib.parse import urlencode

# 添加后端目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, backend_dir)

from backend.app.main import app

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 使用简单的 lambda handler
async def handler(event, context):
    """
    Vercel Serverless Function 处理器
    处理来自 API Gateway 的请求并返回响应
    """
    try:
        # 解析请求信息
        path = event.get('path', '')
        http_method = event.get('httpMethod', '')
        headers = event.get('headers', {})
        query_params = event.get('queryStringParameters', {})
        body = event.get('body', '')
        
        # 如果body是JSON字符串，则解析它
        if body and isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        
        # 构建 ASGI scope
        scope = {
            'type': 'http',
            'method': http_method,
            'path': path,
            'raw_path': path.encode(),
            'headers': [[k.lower().encode(), v.encode()] for k, v in headers.items()],
            'query_string': urlencode(query_params).encode() if query_params else b'',
            'client': ('', 0),
            'server': ('', 0),
            'scheme': 'https',
        }
        
        # 处理请求
        response = await app(scope, lambda: body, lambda x: None)
        
        # 返回响应
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.body.decode()
        }
        
    except Exception as e:
        # 错误处理
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }