"""
Controller para endpoints de email
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
import time

from ..models.email_models import (
    EmailResponse, 
    HealthResponse, 
    CategoriesResponse,
    CategoryInfo
)
from ..services.email_classifier import EmailClassifier
from ..services.file_processor import FileProcessor
from ..utils.config import settings

# Criar router
router = APIRouter()

# Instâncias dos serviços
email_classifier = EmailClassifier()
file_processor = FileProcessor()


@router.get("/", response_model=HealthResponse)
async def root():
    """Endpoint raiz da API"""
    return HealthResponse.create_healthy("AutoU Email Classifier API está funcionando!")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check da API"""
    # Verificar se a API key do OpenAI está configurada
    if not settings.openai_api_key:
        return HealthResponse.create_warning(
            "API configurada, mas OPENAI_API_KEY não encontrada"
        )
    
    return HealthResponse.create_healthy()


@router.get("/categories", response_model=CategoriesResponse)
async def get_categories():
    """Retorna as categorias disponíveis para classificação"""
    categories = [
        CategoryInfo(
            name="produtivo",
            description="Emails que requerem uma ação ou resposta específica",
            examples=[
                "Solicitações de suporte técnico",
                "Atualizações sobre casos em aberto",
                "Dúvidas sobre o sistema",
                "Reclamações ou problemas"
            ]
        ),
        CategoryInfo(
            name="improdutivo",
            description="Emails que não necessitam de uma ação imediata",
            examples=[
                "Mensagens de felicitações",
                "Agradecimentos genéricos",
                "Mensagens de spam",
                "Conteúdo irrelevante"
            ]
        )
    ]
    
    return CategoriesResponse(categories=categories)


@router.post("/classify-email", response_model=EmailResponse)
async def classify_email_endpoint(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    """
    Endpoint principal para classificação de emails
    
    Aceita:
    - Texto direto via form
    - Arquivo (.txt ou .pdf) via upload
    
    Retorna:
    - Categoria do email (produtivo/improdutivo)
    - Resposta automática sugerida
    - Tempo de processamento
    - Tamanho do texto processado
    """
    start_time = time.time()
    
    try:
        # Validar entrada
        if not text and not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="É necessário fornecer texto ou arquivo"
            )
        
        # Processar entrada
        if file:
            # Validar nome do arquivo
            if not file.filename:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nome do arquivo é obrigatório"
                )
            
            # Validar extensão
            if not file_processor.validate_file_extension(file.filename):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Formato não suportado. Use: {', '.join(settings.allowed_extensions)}"
                )
            
            # Ler conteúdo do arquivo
            file_content = await file.read()
            
            # Validar tamanho
            if not file_processor.validate_file_size(file_content):
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"Arquivo muito grande. Máximo permitido: {settings.max_file_size // (1024*1024)}MB"
                )
            
            # Processar arquivo
            email_text = file_processor.process_file_content(file_content, file.filename)
            
        else:
            # Usar texto direto
            if not text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Texto não pode estar vazio"
                )
            email_text = text.strip()
        
        # Verificar se o texto não está muito curto
        if len(email_text) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Texto muito curto. Mínimo de 10 caracteres"
            )
        
        # Classificar email e gerar resposta
        category, suggested_response = email_classifier.classify_and_generate_response(email_text)
        
        # Calcular tempo de processamento
        processing_time = time.time() - start_time
        
        # Retornar resposta
        return EmailResponse(
            category=category,
            suggested_response=suggested_response,
            processing_time=round(processing_time, 3),
            text_length=len(email_text)
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except ValueError as e:
        # Erros de validação
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        # Erros internos
        print(f"Erro interno: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor. Tente novamente."
        )


@router.post("/classify-text", response_model=EmailResponse)
async def classify_text_only(text: str = Form(...)):
    """
    Endpoint simplificado para classificação apenas de texto
    
    Args:
        text: Texto do email para classificar
        
    Returns:
        EmailResponse: Resultado da classificação
    """
    start_time = time.time()
    
    try:
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
        
        # Classificar email e gerar resposta
        category, suggested_response = email_classifier.classify_and_generate_response(text.strip())
        
        # Calcular tempo de processamento
        processing_time = time.time() - start_time
        
        return EmailResponse(
            category=category,
            suggested_response=suggested_response,
            processing_time=round(processing_time, 3),
            text_length=len(text.strip())
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"Erro interno: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor. Tente novamente."
        )
