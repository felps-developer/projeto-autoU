"""
Modelos de dados para emails
"""

from pydantic import BaseModel
from typing import Optional
from enum import Enum
import time


class EmailCategory(str, Enum):
    """Categorias de classificação de emails"""
    PRODUTIVO = "produtivo"
    IMPRODUTIVO = "improdutivo"


class EmailResponse(BaseModel):
    """Modelo de resposta da classificação de email"""
    category: EmailCategory
    suggested_response: str
    processing_time: float
    text_length: int
    
    class Config:
        json_encoders = {
            EmailCategory: lambda v: v.value
        }


class HealthResponse(BaseModel):
    """Modelo de resposta do health check"""
    status: str
    message: str
    timestamp: str
    
    @classmethod
    def create_healthy(cls, message: str = "API funcionando corretamente"):
        return cls(
            status="healthy",
            message=message,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )
    
    @classmethod
    def create_warning(cls, message: str):
        return cls(
            status="warning",
            message=message,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )


class ErrorResponse(BaseModel):
    """Modelo de resposta de erro"""
    error: str
    detail: str
    timestamp: str
    
    @classmethod
    def create(cls, error: str, detail: str = ""):
        return cls(
            error=error,
            detail=detail,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
        )


class CategoryInfo(BaseModel):
    """Informações sobre uma categoria"""
    name: str
    description: str
    examples: list[str]


class CategoriesResponse(BaseModel):
    """Resposta com categorias disponíveis"""
    categories: list[CategoryInfo]
