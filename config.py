import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    COZE_API_URL = os.getenv('COZE_API_URL')
    COZE_API_KEY = os.getenv('COZE_API_KEY')
    IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')
    
    WORKFLOWS = {
        'mood': os.getenv('WORKFLOW_ID_MOOD'),
        'sarcastic': os.getenv('WORKFLOW_ID_SARCASTIC'),
    }
    
    VERCEL_ENV = os.getenv('VERCEL_ENV', 'development')
    VERCEL_URL = os.getenv('VERCEL_URL', 'localhost:5001')
    VERCEL_REGION = os.getenv('VERCEL_REGION', 'dev1')
    VERCEL_DEPLOYMENT_ID = os.getenv('VERCEL_DEPLOYMENT_ID', '')
    
    BASE_URL = f"https://{VERCEL_URL}" if VERCEL_ENV == 'production' else f"http://{VERCEL_URL}"

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production' 