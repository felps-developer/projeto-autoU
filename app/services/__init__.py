"""
Serviços de negócio da aplicação
"""

from .email_classifier import EmailClassifier
from .file_processor import FileProcessor

__all__ = [
    "EmailClassifier",
    "FileProcessor"
]
