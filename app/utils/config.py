"""
Configurações da aplicação
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # API Settings
    app_name: str = "AutoU Email Classifier"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # OpenAI Settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    openai_max_tokens: int = 100
    openai_temperature: float = 0.1
    
    # File Processing Settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: list = [".txt", ".pdf"]
    
    # CORS Settings
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global das configurações
settings = Settings()
