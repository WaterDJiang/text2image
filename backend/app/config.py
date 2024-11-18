import os
from dotenv import load_dotenv
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class Settings:
    """应用配置类"""
    
    def __init__(self):
        # API配置
        self.COZE_API_URL = os.getenv('COZE_API_URL')
        self.COZE_API_KEY = os.getenv('COZE_API_KEY')
        self.IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')
        
        # 工作流ID配置
        self.WORKFLOW_ID_MOOD = os.getenv('WORKFLOW_ID_MOOD')
        self.WORKFLOW_ID_SARCASTIC = os.getenv('WORKFLOW_ID_SARCASTIC')
        self.WORKFLOW_ID_POETRY = os.getenv('WORKFLOW_ID_POETRY')
        self.WORKFLOW_ID_STORY = os.getenv('WORKFLOW_ID_STORY')
        
        # 记录环境变量状态
        self._log_env_status()
        
    def _log_env_status(self):
        """记录环境变量状态"""
        env_vars = {
            'COZE_API_URL': bool(self.COZE_API_URL),
            'COZE_API_KEY': bool(self.COZE_API_KEY),
            'IMGBB_API_KEY': bool(self.IMGBB_API_KEY),
            'WORKFLOW_ID_MOOD': bool(self.WORKFLOW_ID_MOOD),
            'WORKFLOW_ID_SARCASTIC': bool(self.WORKFLOW_ID_SARCASTIC)
        }
        logger.info(f"Environment variables status: {env_vars}")

settings = Settings() 