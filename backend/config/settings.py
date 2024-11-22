import os
from dotenv import load_dotenv

load_dotenv()

# API配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_BASE = os.getenv('DEEPSEEK_API_BASE', "https://api.deepseek.com")

# 图片配置
IMAGE_WIDTH = 360
IMAGE_HEIGHT = 600
