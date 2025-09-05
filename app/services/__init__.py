"""
Serviços de negócio da aplicação
"""

from .email_classifier import EmailClassifier
from .file_processor import FileProcessor
from .email_service import EmailService

__all__ = [
    "EmailClassifier",
    "FileProcessor",
    "EmailService"
]
