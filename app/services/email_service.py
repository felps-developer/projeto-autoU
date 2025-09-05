"""
Service para lógica de negócio de emails
"""

from fastapi import HTTPException, status, UploadFile
import time
from typing import Tuple

from ..models.email_models import EmailResponse, EmailCategory
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
        """
        Valida a entrada do usuário
        
        Args:
            text: Texto do email
            file: Arquivo enviado
            
        Raises:
            HTTPException: Se a validação falhar
        """
        # Verificar se pelo menos um parâmetro foi fornecido
        if not text and not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="É necessário fornecer texto ou arquivo"
            )
        
        # Validar arquivo se fornecido
        if file:
            self._validate_file(file)
        
        # Validar texto se fornecido
        if text:
            self._validate_text(text)
    
    def _validate_file(self, file: UploadFile) -> None:
        """
        Valida o arquivo enviado
        
        Args:
            file: Arquivo a ser validado
            
        Raises:
            HTTPException: Se a validação falhar
        """
        # Verificar nome do arquivo
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome do arquivo é obrigatório"
            )
        
        # Validar extensão
        if not self.file_processor.validate_file_extension(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato não suportado. Use: {', '.join(settings.allowed_extensions)}"
            )
    
    def _validate_text(self, text: str) -> None:
        """
        Valida o texto fornecido
        
        Args:
            text: Texto a ser validado
            
        Raises:
            HTTPException: Se a validação falhar
        """
        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Texto não pode estar vazio"
            )
        
        if len(text.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Texto muito curto. Mínimo de 10 caracteres"
            )
    
    async def process_file_upload(self, file: UploadFile) -> str:
        """
        Processa o upload de arquivo
        
        Args:
            file: Arquivo a ser processado
            
        Returns:
            str: Texto extraído do arquivo
            
        Raises:
            HTTPException: Se o processamento falhar
        """
        try:
            # Ler conteúdo do arquivo
            file_content = await file.read()
            
            # Validar tamanho
            if not self.file_processor.validate_file_size(file_content):
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Arquivo muito grande. Máximo permitido: {settings.max_file_size // (1024*1024)}MB"
                )
            
            # Processar arquivo
            email_text = self.file_processor.process_file_content(file_content, file.filename)
            
            return email_text
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar arquivo: {str(e)}"
            )
    
    def process_text_input(self, text: str) -> str:
        """
        Processa entrada de texto
        
        Args:
            text: Texto a ser processado
            
        Returns:
            str: Texto processado
        """
        return text.strip()
    
    def classify_and_generate_response(self, email_text: str) -> Tuple[EmailCategory, str]:
        """
        Classifica email e gera resposta
        
        Args:
            email_text: Texto do email
            
        Returns:
            Tuple[EmailCategory, str]: Categoria e resposta gerada
        """
        try:
            return self.email_classifier.classify_and_generate_response(email_text)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro na classificação: {str(e)}"
            )
    
    def create_email_response(
        self, 
        category: EmailCategory, 
        suggested_response: str, 
        processing_time: float, 
        text_length: int
    ) -> EmailResponse:
        """
        Cria resposta da classificação
        
        Args:
            category: Categoria do email
            suggested_response: Resposta sugerida
            processing_time: Tempo de processamento
            text_length: Tamanho do texto
            
        Returns:
            EmailResponse: Resposta formatada
        """
        return EmailResponse(
            category=category,
            suggested_response=suggested_response,
            processing_time=round(processing_time, 3),
            text_length=text_length
        )
    
    async def process_email_classification(
        self, 
        text: str = None, 
        file: UploadFile = None
    ) -> EmailResponse:
        """
        Processa classificação de email completa
        
        Args:
            text: Texto do email
            file: Arquivo do email
            
        Returns:
            EmailResponse: Resultado da classificação
        """
        start_time = time.time()
        
        # Validar entrada
        self.validate_input(text, file)
        
        # Processar entrada
        if file:
            email_text = await self.process_file_upload(file)
        else:
            email_text = self.process_text_input(text)
        
        # Classificar e gerar resposta
        category, suggested_response = self.classify_and_generate_response(email_text)
        
        # Calcular tempo de processamento
        processing_time = time.time() - start_time
        
        # Criar e retornar resposta
        return self.create_email_response(
            category=category,
            suggested_response=suggested_response,
            processing_time=processing_time,
            text_length=len(email_text)
        )
