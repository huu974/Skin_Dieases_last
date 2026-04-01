"""
应用配置管理
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "智肤康·皮肤疾病AI全流程辅助诊疗系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DATABASE: str = "skin_diagnosis"
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = ["jpg", "jpeg", "png", "bmp", "webp"]
    
    # AI模型配置
    MODEL_PATH: str = "E:/py项目/Skin diseases/model"
    YOLO_MODEL: str = "E:/py项目/Skin diseases/yolo_variables/checkpoint_yolo.pt"
    CLASSIFICATION_MODEL: str = "E:/py项目/Skin diseases/variables/best_model.pth.tar"
    
    # LLM配置
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4"
    
    # 向量数据库配置
    VECTOR_DB_PATH: str = "E:/py项目/Skin diseases/chroma_db"
    
    # 加密配置
    ENCRYPTION_KEY: str = "32-char-encryption-key-here!!!"
    
    # 地图API配置
    MAP_API_KEY: str = ""
    
    # 性能配置
    DIAGNOSIS_TIMEOUT: int = 3  # 秒
    CHAT_TIMEOUT: int = 2  # 秒
    MAX_CONCURRENT: int = 1000
    
    # 多模式配置
    SYSTEM_MODES: list = ["production", "development", "test", "demo"]
    DEFAULT_MODE: str = "production"
    
    @property
    def DATABASE_URL(self) -> str:
        # return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        return "sqlite:///./skin_diagnosis.db"
    
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
