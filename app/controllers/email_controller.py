"""
Controller para endpoints de email
"""

from fastapi import APIRouter, UploadFile, File, Form

from ..models.email_models import (
    EmailResponse, 
    HealthResponse, 
    CategoriesResponse,
    CategoryInfo
)
from ..services.email_service import EmailService
from ..utils.config import settings

# Criar router
router = APIRouter()

# Instância do service
email_service = EmailService()


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
    return await email_service.process_email_classification(text=text, file=file)


@router.post("/classify-text", response_model=EmailResponse)
async def classify_text_only(text: str = Form(...)):
    """
    Endpoint simplificado para classificação apenas de texto
    
    Args:
        text: Texto do email para classificar
        
    Returns:
        EmailResponse: Resultado da classificação
    """
    return await email_service.process_email_classification(text=text)
