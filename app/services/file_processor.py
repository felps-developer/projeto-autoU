"""
Serviço para processamento de arquivos de email
"""

import PyPDF2
from io import BytesIO
import re
from typing import Optional
from ..utils.config import settings


class FileProcessor:
    """Classe para processamento de arquivos"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extrai texto de arquivo PDF
        
        Args:
            file_content: Conteúdo do arquivo PDF em bytes
            
        Returns:
            str: Texto extraído do PDF
        """
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
        """
        Extrai texto de arquivo TXT
        
        Args:
            file_content: Conteúdo do arquivo TXT em bytes
            
        Returns:
            str: Texto extraído do TXT
        """
        try:
            # Tentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    return file_content.decode(encoding)
                except UnicodeDecodeError:
                    continue
            
            # Se nenhum encoding funcionar, usar utf-8 com tratamento de erro
            return file_content.decode('utf-8', errors='replace')
        
        except Exception as e:
            raise ValueError(f"Erro ao extrair texto do arquivo TXT: {str(e)}")
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Limpa e normaliza o texto do email
        
        Args:
            text: Texto bruto do email
            
        Returns:
            str: Texto limpo e normalizado
        """
        if not text:
            return ""
        
        # Remover quebras de linha excessivas
        text = re.sub(r'\n+', ' ', text)
        
        # Remover espaços em branco excessivos
        text = re.sub(r'\s+', ' ', text)
        
        # Remover caracteres especiais desnecessários
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)]', '', text)
        
        # Limpar espaços no início e fim
        text = text.strip()
        
        return text
    
    @staticmethod
    def validate_email_content(text: str) -> bool:
        """
        Valida se o texto contém conteúdo válido de email
        
        Args:
            text: Texto a ser validado
            
        Returns:
            bool: True se o texto é válido, False caso contrário
        """
        if not text or len(text.strip()) < 10:
            return False
        
        # Verificar se contém pelo menos algumas palavras
        words = text.split()
        if len(words) < 3:
            return False
        
        return True
    
    @classmethod
    def process_file_content(cls, file_content: bytes, filename: str) -> str:
        """
        Processa o conteúdo de um arquivo e retorna o texto limpo
        
        Args:
            file_content: Conteúdo do arquivo em bytes
            filename: Nome do arquivo
            
        Returns:
            str: Texto processado e limpo
            
        Raises:
            ValueError: Se o formato do arquivo não for suportado
        """
        if not filename:
            raise ValueError("Nome do arquivo é obrigatório")
        
        filename_lower = filename.lower()
        
        if filename_lower.endswith('.pdf'):
            text = cls.extract_text_from_pdf(file_content)
        elif filename_lower.endswith('.txt'):
            text = cls.extract_text_from_txt(file_content)
        else:
            raise ValueError("Formato de arquivo não suportado. Use .pdf ou .txt")
        
        # Limpar o texto
        cleaned_text = cls.clean_text(text)
        
        # Validar o conteúdo
        if not cls.validate_email_content(cleaned_text):
            raise ValueError("O arquivo não contém conteúdo válido de email")
        
        return cleaned_text
    
    @staticmethod
    def validate_file_size(file_content: bytes) -> bool:
        """
        Valida o tamanho do arquivo
        
        Args:
            file_content: Conteúdo do arquivo
            
        Returns:
            bool: True se o tamanho é válido
        """
        return len(file_content) <= settings.max_file_size
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """
        Valida a extensão do arquivo
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            bool: True se a extensão é válida
        """
        if not filename:
            return False
        
        filename_lower = filename.lower()
        return any(filename_lower.endswith(ext) for ext in settings.allowed_extensions)
