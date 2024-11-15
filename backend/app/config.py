import os
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Settings:
    """应用配置类"""
    
    # API配置
    COZE_API_URL = os.getenv('COZE_API_URL')  # Coze API地址
    COZE_API_KEY = os.getenv('COZE_API_KEY')  # Coze API密钥
    IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')  # ImgBB API密钥
    
    # 工作流ID配置
    WORKFLOW_ID_MOOD = os.getenv('WORKFLOW_ID_MOOD')  # 心情文案工作流
    WORKFLOW_ID_SARCASTIC = os.getenv('WORKFLOW_ID_SARCASTIC')  # 毒舌文案工作流
    WORKFLOW_ID_POETRY = os.getenv('WORKFLOW_ID_POETRY')  # 诗意工作流
    WORKFLOW_ID_STORY = os.getenv('WORKFLOW_ID_STORY')  # 故事工作流
    
    # 服务器配置
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'  # 调试模式
    PORT = int(os.getenv('PORT', 8000))  # 服务端口

    def validate(self):
        """验证必要的配置是否存在"""
        required_fields = [
            'COZE_API_URL',
            'COZE_API_KEY',
            'IMGBB_API_KEY',
            'WORKFLOW_ID_MOOD',
            'WORKFLOW_ID_SARCASTIC'
        ]
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"缺少必要的配置项: {field}")

settings = Settings()
# 验证配置
settings.validate() 