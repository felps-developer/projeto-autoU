"""
Configurações da aplicação
"""

import os
from typing import Optional, List


class Settings:
    """Configurações da aplicação"""
    
    def __init__(self):
        # API Settings
        self.app_name: str = "AutoU Email Classifier"
        self.app_version: str = "1.0.0"
        self.debug: bool = False
        
        # OpenAI Settings
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        # File Processing Settings
        self.max_file_size: int = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions: List[str] = [".txt", ".pdf"]
        
        # CORS Settings
        self.cors_origins: List[str] = ["*"]


# Instância global das configurações
settings = Settings()
