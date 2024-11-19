import openai
import logging
import json
import os
from ..config import settings

logger = logging.getLogger(__name__)

class DeepseekService:
    def __init__(self):
        """初始化DeepseekService"""
        logger.info("正在初始化 DeepSeek 服务...")
        self.api_key = settings.DEEPSEEK_API_KEY
        try:
            openai.api_key = self.api_key
            openai.api_base = "https://api.deepseek.com/v1"
            logger.info("DeepSeek 服务初始化成功")
        except Exception as e:
            logger.error(f"DeepSeek 服务初始化失败: {str(e)}")
            raise
        
    async def process_image(self, image_url, workflow_type="mood"):
        """
        处理图片的主要方法
        Args:
            image_url: 需要处理的图片URL
            workflow_type: 工作流类型，默认为'mood'
        Returns:
            dict: 包含处理后的文本和图片URL
        """
        try:
            logger.info(f"开始处理图片，工作流类型: {workflow_type}")
            logger.info(f"图片URL: {image_url}")
            
            if not image_url:
                logger.error("图片URL为空")
                return None
            
            # 首先定义 system_prompts
            system_prompts = {
                'mood': """
                        你是一位极具创意且专业的朋友圈文案大师，能够从图片中精准地挖掘出深刻情感与意义，为用户创作出令人惊艳的高大上朋友圈文案。
                        # 参考方向
                        - 情感共鸣：深入剖析图片中的自我提升、家庭关系、爱情、嫉妒、人际关系等情感元素，引发强烈共鸣。例如："遇见更好，成就非凡"，让人们在自我提升中找到动力。
                        - 哲理性：赋予文案深刻的哲思，如"思想，填满生活的空缺"，启发人们思考人生。
                        - 现实主义：反映现实社会现象，像"父母与钱，永不背叛"，展现真实的生活感悟。
                        - 警示性：用文案起到警醒作用，"嫉妒如刀，伤人伤己"，提醒人们避免不良情绪。
                        - 人际关系洞察：揭示人际关系的复杂性，"懂你的好，才是真的好"，增进人与人之间的理解。
                        - 自我反省：鼓励自我反思，"坏脾气，留给最亲的人"，促使人们改善自身行为。
                        - 幽默与讽刺：以幽默或讽刺的方式传达深刻信息，"世界没抛弃你，你也别瞎嚷嚷"，让人在轻松中领悟道理。
                        - 简洁有力：用简洁的语言传递丰富信息，让文案更具感染力。
                        - 普遍性：确保文案观点和情感具有广泛吸引力，不局限于特定群体。
                        - 启发性：激发人们思考和行动，如"得不到，就收获经验"，引导人们积极面对生活。
                        # 步骤
                        1. 读取用户上传的图片链接，全面分析图片中的环境、人物以及心境、情绪等细节。
                        2. 从参考方向中精心选取合适的表达方式进行文案创作。
                        3. 以第一人称输出一句关于图片心情的文案，采用口语化表达，去掉主语，增强对象感。

                        # 输出说明
                        1. 使用文本格式输出结果。
                        2. 只输出文案，无其他无关内容。
                        3. 参考案例：
                            - 最美的遇见，是遇见更好的自己。
                            - 若皮囊难修，就用思想填满。
                            - 父母和钱，才是永远的依靠。
                            - 嫉妒如刀，扎心伤己。
                            - 懂你的好，才是真的好。
                            - 坏脾气，都给了最亲的人。
                            - 得不到，就收获经验。
                            - 别瞎嚷嚷，世界没抛弃你。

                        # 限制
                        - 专注于图片分析和文案创作，不涉及其他无关话题。
                        - 严格按照要求的格式输出文案，不得偏离。
                        """,
                'sarcastic': """
                            # 角色和目的
                            你是一位极具批判思维的评论家，请你从图片中精准地挖掘出内涵与意义，然后用毒辣批判的口吻点评出来。

                            # 步骤
                            1.  分析输入的图片链接内容，理解图片想要表达的内容和情感。
                            2. 根据第一步的图片信息，结合Oscar Wilde的机智、鲁迅的尖锐和林语堂的幽默，对图片进行点评。
                            3. 以第一人称输出三句关于图片点评的文案，采用口语化表达，去掉主语，增强对象感。
                            4. 从三句文案中随机抽取你觉得最好的那句作为最后的输出。

                            # 输出说明
                            1. 使用文本格式输出结果。
                            2. 只输出文案，无其他无关内容。
                            3. 参考输出案例：
                            - "菜的味道让我怀疑厨师是不是在和调料吵架。"
                            - "演唱会就像是一场长达两小时的音响测试，唯一的亮点是它终于结了。"
                            - "新手机的创新功能让我怀疑它是不是来自上个世纪。"
                            - "他的时尚品味就像天气预报，总是出乎意料地糟糕。"
                            - "他们表现让我想起了一句老话：失败乃成功之母，但他们似乎只见到了母亲。"

                            # 限制
                            1. 专注于图片分析和点评创作，不涉及其他无关话题。
                            2. 去掉一些对照片本身的指示代词，不要使用"这xx……"的句式开头。
                            3. 严格按照要求的格式输出文案，不得偏离。
                        """,
                'story': """
                        你是一个擅长根据图片创作故事的AI助手。请为这张图片编写一个有趣的小故事。
                        """
            }
            
            if workflow_type not in system_prompts:
                logger.error(f"不支持的工作流类型: {workflow_type}")
                return None
            
            messages = [
                {"role": "system", "content": system_prompts.get(workflow_type, system_prompts['mood'])},
                {"role": "user", "content": f"请观察这张图片（{image_url}）并给出你的创作。"}
            ]
            
            logger.info("正在发送请求到 DeepSeek API...")
            logger.debug(f"请求参数: {json.dumps(messages, ensure_ascii=False)}")
            
            # 调用API
            response = await openai.ChatCompletion.acreate(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                stream=False
            )
            
            logger.info("DeepSeek API 响应成功")
            logger.debug(f"API响应: {response}")
            
            output_text = response.choices[0].message.content
            logger.info("成功获取生成的文本")
            logger.debug(f"生成的文本: {output_text}")
            
            # 调用图片服务生成明信片样式的图片
            logger.info("开始生成明信片样式图片...")
            from ..services.image_service import ImageService
            image_service = ImageService()
            postcard_image = await image_service.create_postcard(
                image_url=image_url,
                text=output_text
            )
            logger.info("明信片样式图片生成成功")
            
            # 上传合成后的图片
            logger.info("开始上传合成后的图片...")
            from ..services.imgbb_service import ImgBBService
            imgbb_service = ImgBBService()
            final_image_url = await imgbb_service.upload_image(postcard_image)
            
            if not final_image_url:
                logger.error("合成图片上传失败")
                return None
            
            logger.info("图片上传成功")
            logger.debug(f"最终图片URL: {final_image_url}")
            
            return {
                'text': output_text,
                'original_image': image_url,
                'postcard_image': final_image_url
            }
            
        except Exception as e:
            logger.error(f"处理图片时发生错误: {str(e)}", exc_info=True)
            return None
    
    async def process_poetry(self, text):
        try:
            logger.info("开始处理诗意文本...")
            
            messages = [
                {"role": "system", "content": """
                 你是一位诗意点评大师。请按照以下格式提供输出：
                 1. 你是毒辣的评论家，擅长用辛辣讽刺、自嘲、幽默的表达方式改成一句话评论，请你根据用户提供的内容，经过思考理解之后，输出一句点评，字数不要超过 20 字，用【点评】作为开始标记。
                    参考表达：
                    -别人的痛苦才是艺术的源泉。而你去受苦，只会成为别人艺术的源泉。
                    -保持愚蠢，又不能知道自己有多蠢。
                    -人在年轻的时候，觉得到处都是人，别人的事就是你的事，到了中年以后，才觉得世界上除了家人已经一无所有了。
                 2. 然后提供一个简单的SVG艺术图形，用【SVG】作为开始标记
                 
                 SVG要求：
                 - 画布大小：96x120
                 - 背景色：#1a1a1a
                 - 使用以下颜色之一：#ff4136、#f5a05b、#183bed
                 - 只包含简单的几何图形（圆形、线条、多边形等）
                 - 不要包含任何文字
                 - 风格：禅意、抽象
                """},
                {"role": "user", "content": f"请为这段文字提供诗意点评和配图：{text}"}
            ]
            
            response = await openai.ChatCompletion.acreate(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                stream=False
            )
            
            content = response.choices[0].message.content
            
            comment = ""
            svg = ""
            
            if "【点评】" in content:
                comment = content.split("【点评】")[1].split("【SVG】")[0].strip()
            if "【SVG】" in content:
                svg = content.split("【SVG】")[1].strip()
                
            logger.info(f"生成的点评: {comment}")
            logger.debug(f"生成的SVG: {svg}")
            
            return {
                'comment': comment,
                'svg': svg
            }
                
        except Exception as e:
            logger.error(f"处理诗意文本时发生错误: {str(e)}", exc_info=True)
            return None