from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    COZE_API_URL: str
    COZE_API_KEY: str
    IMGBB_API_KEY: str
    WORKFLOW_ID_MOOD: str
    WORKFLOW_ID_SARCASTIC: str
    WORKFLOW_ID_POETRY: str
    WORKFLOW_ID_STORY: str
    DEEPSEEK_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings() 