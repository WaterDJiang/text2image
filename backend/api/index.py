# from fastapi import FastAPI
# from mangum import Mangum
# from fastapi.middleware.cors import CORSMiddleware
# import sys
# import os

# # 添加后端目录到 Python 路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# backend_dir = os.path.dirname(os.path.dirname(current_dir))
# sys.path.insert(0, backend_dir)

# from backend.app.main import app

# # 配置 CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 创建 handler
# handler = Mangum(app, lifespan="off")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

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
    import json
    from urllib.parse import urlencode
    
    path = event.get('path', '')
    http_method = event.get('httpMethod', '')
    headers = event.get('headers', {})
    query_string = event.get('queryStringParameters', {})
    body = event.get('body', '')
    
    # 构建 ASGI scope
    scope = {
        'type': 'http',
        'method': http_method,
        'path': path,
        'headers': [[k.lower().encode(), v.encode()] for k, v in headers.items()],
        'query_string': urlencode(query_string).encode() if query_string else b'',
    }
    
    # 处理请求
    response = await app(scope, lambda: body, lambda x: None)
    
    # 返回响应
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.body.decode()
    }