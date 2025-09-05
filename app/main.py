"""
Aplicação principal FastAPI do AutoU Email Classifier
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import os

from .controllers.email_controller import router
from .models.email_models import ErrorResponse
from .utils.config import settings

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API para classificação de emails e geração de respostas automáticas",
    version=settings.app_version,
    debug=settings.debug
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requisições"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    print(f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
    
    return response


# Incluir rotas
app.include_router(router)


# Handler de erros global
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para erros gerais"""
    print(f"Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse.create(
            error="Erro interno do servidor",
            detail="Ocorreu um erro inesperado. Tente novamente."
        ).dict()
    )


# Executar aplicação
if __name__ == "__main__":
    import uvicorn
    
    # Verificar se a API key está configurada
    if not settings.openai_api_key:
        print("⚠️  AVISO: OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        print("   Crie um arquivo .env com: OPENAI_API_KEY=sua_chave_aqui")
        print("   A aplicação funcionará com classificação por palavras-chave como fallback")
    
    print("🚀 Iniciando AutoU Email Classifier API...")
    print("📖 Documentação disponível em: http://localhost:8000/docs")
    print("🔍 Health check em: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
