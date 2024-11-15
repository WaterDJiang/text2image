import requests
import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class CozeService:
    def __init__(self):
        self.api_url = os.getenv('COZE_API_URL')
        self.api_key = os.getenv('COZE_API_KEY')
        self.workflow_id_mood = os.getenv('WORKFLOW_ID_MOOD')
        self.workflow_id_sarcastic = os.getenv('WORKFLOW_ID_SARCASTIC')
    
    def process_image(self, image_url, workflow_type="mood"):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Connection": "keep-alive"
            }
            
            workflow_id = self.workflow_id_mood if workflow_type == "mood" else self.workflow_id_sarcastic
            
            # 记录输入参数
            logger.debug(f"处理图片 - 工作流类型: {workflow_type}")
            logger.debug(f"处理图片 - 输入URL: {image_url}")
            logger.debug(f"处理图片 - 工作流ID: {workflow_id}")
            
            payload = {
                "workflow_id": workflow_id,
                "parameters": {
                    "image_url": image_url
                }
            }
            
            # 记录完整请求
            logger.debug(f"Coze API请求: {payload}")
            
            response = requests.post(self.api_url, json=payload, headers=headers)
            logger.debug(f"Coze API响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.debug(f"Coze API完整响应: {result}")
                
                if result.get('code') == 0:
                    try:
                        data = json.loads(result.get('data', '{}'))
                        logger.debug(f"解析后的数据: {data}")
                        
                        output_url = data.get('output')
                        if output_url:
                            logger.debug(f"获取到的输出图片URL: {output_url}")
                            return {
                                'output_image_url': output_url,
                                'debug_url': result.get('debug_url')
                            }
                        else:
                            logger.error("响应中未找到output字段")
                            return None
                            
                    except json.JSONDecodeError as e:
                        logger.error(f"解析Coze返回数据失败: {e}")
                        return None
                else:
                    logger.error(f"Coze API调用失败: {result.get('msg')}")
                    return None
            elif response.status_code == 504:
                logger.error("Coze API调用超时")
                return None
            else:
                logger.error(f"Coze API请求失败: HTTP {response.status_code}")
                logger.error(f"错误响应: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求Coze API时发生错误: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"处理图片时发生未预期的错误: {str(e)}")
            return None 