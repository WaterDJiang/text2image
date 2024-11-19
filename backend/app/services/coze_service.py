import requests
import os
import json
import logging
from dotenv import load_dotenv
import httpx

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

class CozeService:
    def __init__(self):
        """初始化CozeService，从环境变量获取配置"""
        logger.info("正在初始化 Coze 服务...")
        
        # 从环境变量获取配置
        self.api_url = os.getenv('COZE_API_URL', 'https://api.coze.cn/v1/workflow/run')
        self.api_key = os.getenv('COZE_API_KEY')
        self.workflow_id_mood = os.getenv('WORKFLOW_ID_MOOD')
        self.workflow_id_sarcastic = os.getenv('WORKFLOW_ID_SARCASTIC')
        self.workflow_id_poetry = os.getenv('WORKFLOW_ID_POETRY')
        
        # 验证必要的环境变量
        if not self.api_key:
            raise ValueError("COZE_API_KEY 环境变量未设置")
        if not self.api_key.startswith('pat_'):
            raise ValueError("COZE_API_KEY 必须以 'pat_' 开头")
            
        logger.info("Coze 服务初始化成功")
    
    async def process_image(self, image_url: str, workflow_type: str = "mood") -> dict:
        """异步处理图片"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "*/*"
            }
            
            workflow_id = self._get_workflow_id(workflow_type)
            if not workflow_id:
                logger.error(f"未找到工作流类型: {workflow_type}")
                return None
            
            payload = {
                "workflow_id": workflow_id,
                "parameters": {
                    "image_url": image_url
                },
                "is_async": False
            }
            
            logger.debug("Coze API请求信息:")
            logger.debug(f"URL: {self.api_url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,  # 直接使用完整 URL，不添加 /process
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response content: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('code') == 0:
                        try:
                            data = result.get('data')
                            if isinstance(data, str):
                                data = json.loads(data)
                            
                            logger.debug(f"解析后的数据: {data}")
                            
                            # 获取output中的内容
                            comment = data.get('output', '')
                            svg = data.get('output1', '')
                            
                            return {
                                'comment': comment,
                                'svg': svg,
                                'debug_url': result.get('debug_url')
                            }
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON解析失败: {str(e)}, 原始数据: {data}")
                            return None
                    else:
                        logger.error(f"Coze API返回错误码: {result.get('code')}, 消息: {result.get('msg')}")
                        return None
                else:
                    logger.error(f"API请求失败: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"处理图片时发生错误: {str(e)}")
            return None
            
    def _get_workflow_id(self, workflow_type):
        """根据工作流类型获取对应的workflow_id"""
        workflow_map = {
            'mood': self.workflow_id_mood,
            'sarcastic': self.workflow_id_sarcastic
        }
        workflow_id = workflow_map.get(workflow_type)
        logger.debug(f"工作流类型: {workflow_type}, 对应ID: {workflow_id}")
        return workflow_id
    
    async def process_poetry(self, text):
        """处理诗意文本"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "workflow_id": self.workflow_id_poetry,
                "parameters": {
                    "BOT_USER_INPUT": text
                }
            }
            
            logger.info(f"发送请求到 Coze API:")
            logger.info(f"URL: {self.api_url}")
            logger.info(f"Workflow ID: {self.workflow_id_poetry}")
            logger.info(f"Input text: {text}")
            logger.info(f"Headers: {headers}")
            logger.info(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,  # 直接使用完整 URL，不添加 /process
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                # 添加详细的响应日志
                logger.info(f"Coze API 响应状态码: {response.status_code}")
                logger.info(f"Coze API 响应头: {dict(response.headers)}")
                logger.info(f"Coze API 响应内容: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('code') == 0:
                        try:
                            data = result.get('data')
                            if isinstance(data, str):
                                data = json.loads(data)
                            
                            logger.debug(f"解析后的数据: {data}")
                            
                            # 获取output中的内容
                            comment = data.get('output', '')
                            svg = data.get('output1', '')
                            
                            return {
                                'comment': comment,
                                'svg': svg,
                                'debug_url': result.get('debug_url')
                            }
                        except json.JSONDecodeError as e:
                            logger.error(f"JSON解析失败: {str(e)}, 原始数据: {data}")
                            return None
                    else:
                        logger.error(f"Coze API返回错误码: {result.get('code')}, 消息: {result.get('msg')}")
                        return None
                else:
                    error_msg = f"Coze API请求失败: HTTP {response.status_code}, 响应: {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"处理诗意文本时发生错误: {str(e)}")
            raise Exception(f"生成失败: {str(e)}")