import requests
import os
import json
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class CozeService:
    def __init__(self):
        """初始化CozeService，设置API相关配置"""
        self.api_url = settings.COZE_API_URL  # COZE API地址
        self.api_key = settings.COZE_API_KEY  # COZE API密钥
        self.workflow_id_mood = settings.WORKFLOW_ID_MOOD  # 心情工作流ID
        self.workflow_id_sarcastic = settings.WORKFLOW_ID_SARCASTIC  # 毒舌工作流ID
        self.workflow_id_poetry = os.getenv('WORKFLOW_ID_POETRY')  # 诗意工作流ID
    
    def process_image(self, image_url, workflow_type="mood"):
        """
        处理图片的主要方法
        Args:
            image_url: 需要处理的图片URL
            workflow_type: 工作流类型，默认为'mood'
        Returns:
            dict: 包含处理后的图片URL和调试URL
            None: 处理失败时返回
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",  # 设置授权头
                "Content-Type": "application/json",  # 设置内容类型
                "Accept": "*/*"  # 接受所有类型
            }
            
            workflow_id = self._get_workflow_id(workflow_type)  # 获取工作流ID
            if not workflow_id:
                logger.error(f"未找到工作流类型: {workflow_type}")  # 记录错误
                return None
            
            payload = {
                "workflow_id": workflow_id,  # 工作流ID
                "parameters": {
                    "image_url": image_url  # 图片URL
                },
                "is_async": False  # 同步处理
            }
            
            logger.debug("Coze API请求信息:")  # 记录请求信息
            logger.debug(f"URL: {self.api_url}")  # 记录请求URL
            logger.debug(f"Headers: {headers}")  # 记录请求头
            logger.debug(f"Payload: {json.dumps(payload, ensure_ascii=False)}")  # 记录请求体
            
            response = requests.post(self.api_url, json=payload, headers=headers)  # 发送请求
            
            logger.debug(f"Coze API响应状态码: {response.status_code}")  # 记录响应状态码
            logger.debug(f"Coze API响应内容: {response.text}")  # 记录响应内容
            
            if response.status_code == 200:
                result = response.json()  # 解析响应为JSON
                
                if result.get('code') == 0:
                    try:
                        data = result.get('data')  # 获取数据
                        if isinstance(data, str):
                            data = json.loads(data)  # 如果数据是字符串，解析为JSON
                            logger.debug(f"解析后的数据: {data}")  # 记录解析后的数据
                        
                        output_text = data.get('output')  # 获取输出文本
                        if not output_text:
                            logger.error("响应中没有output字段")  # 记录错误
                            return None
                        
                        # 调用图片服务生成明信片样式的图片
                        from ..services.image_service import ImageService
                        image_service = ImageService()
                        postcard_image = image_service.create_postcard(
                            image_url=image_url,
                            text=output_text
                        )
                        
                        # 上传合成后的图片
                        from ..services.imgbb_service import ImgBBService
                        imgbb_service = ImgBBService()
                        final_image_url = imgbb_service.upload_image(postcard_image)
                        
                        if not final_image_url:
                            logger.error("合成图片上传失败")
                            return None
                        
                        return {
                            'text': output_text,
                            'original_image': image_url,
                            'postcard_image': final_image_url,
                            'debug_url': result.get('debug_url')
                        }
                        
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON解析失败: {str(e)}, 原始数据: {data}")
                        return None
                else:
                    logger.error(f"Coze API返回错误码: {result.get('code')}, 消息: {result.get('msg')}")
                    return None
            elif response.status_code == 504:
                logger.error("Coze API执行超时")
                return None
            else:
                logger.error(f"Coze API请求失败: HTTP {response.status_code}")
                logger.error(f"错误响应: {response.text}")
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
    
    def process_poetry(self, text):
        """处理诗意文本，返回评论和SVG图片"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "*/*"
            }
            
            # 构建请求体，使用正确的参数名称
            payload = {
                "workflow_id": self.workflow_id_poetry,
                "parameters": {
                    "BOT_USER_INPUT": text  # 修改为 input_text
                }
            }
            
            logger.debug(f"诗意处理 - 输入文本: {text}")
            logger.debug(f"请求payload: {json.dumps(payload, ensure_ascii=False)}")
            
            response = requests.post(self.api_url, json=payload, headers=headers)
            logger.debug(f"Coze API响应状态码: {response.status_code}")
            logger.debug(f"Coze API响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    try:
                        # 获取data字段
                        data = result.get('data')
                        if isinstance(data, str):
                            data = json.loads(data)
                        
                        logger.debug(f"解析后的数据: {data}")
                        
                        # 获取output1中的内容
                        svg_content = data.get('output1', '')
                        
                        # 提取SVG标签内的内容
                        import re
                        svg_match = re.search(r'(<svg.*?</svg>)', svg_content, re.DOTALL)
                        svg = svg_match.group(1) if svg_match else ''
                        
                        logger.debug(f"提取的SVG: {svg}")
                        
                        return {
                            'comment': data.get('output', ''),
                            'svg': svg,
                            'debug_url': result.get('debug_url')
                        }
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON解析失败: {str(e)}, 原始数据: {data}")
                        if isinstance(data, dict):
                            svg_content = data.get('output1', '')
                            svg_match = re.search(r'(<svg.*?</svg>)', svg_content, re.DOTALL)
                            svg = svg_match.group(1) if svg_match else ''
                            return {
                                'comment': data.get('output', ''),
                                'svg': svg,
                                'debug_url': result.get('debug_url')
                            }
                        return None
                else:
                    logger.error(f"Coze API返回错误码: {result.get('code')}, 消息: {result.get('msg')}")
                    return None
            
            logger.error(f"Coze API请求失败: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"处理诗意文本时发生错误: {str(e)}")
            return None