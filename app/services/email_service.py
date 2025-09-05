"""
Service para lógica de negócio de emails
"""

from fastapi import HTTPException, status, UploadFile
import time

from ..models.email_models import EmailResponse
from .email_classifier import EmailClassifier
from .file_processor import FileProcessor
from ..utils.config import settings


class EmailService:
    """Service para lógica de negócio de emails"""
    
    def __init__(self):
        """Inicializa o service"""
        self.email_classifier = EmailClassifier()
        self.file_processor = FileProcessor()
    
    def validate_input(self, text: str = None, file: UploadFile = None) -> None:
        """Valida a entrada do usuário"""
        if not text and not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="É necessário fornecer texto ou arquivo"
            )
        
        if file and not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome do arquivo é obrigatório"
            )
        
        if file and not self.file_processor.validate_file_extension(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato não suportado. Use: {', '.join(settings.allowed_extensions)}"
            )
        
        if text and (not text.strip() or len(text.strip()) < 10):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Texto muito curto. Mínimo de 10 caracteres"
            )
    
    async def process_email_classification(
        self, 
        text: str = None, 
        file: UploadFile = None
    ) -> EmailResponse:
        """Processa classificação de email completa"""
        start_time = time.time()
        
        # Validar entrada
        self.validate_input(text, file)
        
        # Processar entrada
        if file:
            file_content = await file.read()
            if not self.file_processor.validate_file_size(file_content):
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Arquivo muito grande. Máximo: {settings.max_file_size // (1024*1024)}MB"
                )
            email_text = self.file_processor.process_file_content(file_content, file.filename)
        else:
            email_text = text.strip()
        
        # Classificar e gerar resposta
        try:
            category, suggested_response = self.email_classifier.classify_and_generate_response(email_text)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro na classificação: {str(e)}"
            )
        
        # Retornar resposta
        return EmailResponse(
            category=category,
            suggested_response=suggested_response,
            processing_time=round(time.time() - start_time, 3),
            text_length=len(email_text)
        )