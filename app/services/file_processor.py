"""
Serviço para processamento de arquivos de email
"""

import PyPDF2
from io import BytesIO
import re
from ..utils.config import settings


class FileProcessor:
    """Classe para processamento de arquivos"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extrai texto de arquivo PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Erro ao extrair texto do PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """Extrai texto de arquivo TXT"""
        try:
            encodings = ['utf-8', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    return file_content.decode(encoding)
                except UnicodeDecodeError:
                    continue
            return file_content.decode('utf-8', errors='replace')
        except Exception as e:
            raise ValueError(f"Erro ao extrair texto do arquivo TXT: {str(e)}")
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Limpa e normaliza o texto"""
        if not text:
            return ""
        
        # Remover quebras de linha excessivas e espaços
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)]', '', text)
        
        return text.strip()
    
    @staticmethod
    def validate_email_content(text: str) -> bool:
        """Valida se o texto contém conteúdo válido"""
        if not text or len(text.strip()) < 10:
            return False
        words = text.split()
        return len(words) >= 3
    
    @classmethod
    def process_file_content(cls, file_content: bytes, filename: str) -> str:
        """Processa o conteúdo de um arquivo"""
        if not filename:
            raise ValueError("Nome do arquivo é obrigatório")
        
        filename_lower = filename.lower()
        
        if filename_lower.endswith('.pdf'):
            text = cls.extract_text_from_pdf(file_content)
        elif filename_lower.endswith('.txt'):
            text = cls.extract_text_from_txt(file_content)
        else:
            raise ValueError("Formato não suportado. Use .pdf ou .txt")
        
        cleaned_text = cls.clean_text(text)
        
        if not cls.validate_email_content(cleaned_text):
            raise ValueError("O arquivo não contém conteúdo válido de email")
        
        return cleaned_text
    
    @staticmethod
    def validate_file_size(file_content: bytes) -> bool:
        """Valida o tamanho do arquivo"""
        return len(file_content) <= settings.max_file_size
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """Valida a extensão do arquivo"""
        if not filename:
            return False
        filename_lower = filename.lower()
        return any(filename_lower.endswith(ext) for ext in settings.allowed_extensions)