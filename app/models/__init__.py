"""
Modelos de dados da aplicação
"""

from .email_models import EmailCategory, EmailResponse, HealthResponse, ErrorResponse

__all__ = [
    "EmailCategory",
    "EmailResponse", 
    "HealthResponse",
    "ErrorResponse"
]
