"""
Aplicação principal FastAPI
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from .controllers.email_controller import router
from .models.email_models import ErrorResponse, HealthResponse
from .utils.config import settings

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API para classificação de emails e geração de respostas automáticas",
    version=settings.app_version,
    debug=settings.debug
)

# CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router)

# Middleware para log de requisições e tratamento de erros
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 3))
        return response
    except Exception as e:
        # Log do erro
        print(f"Erro na requisição: {request.url} - {str(e)}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                message="Erro interno do servidor. Tente novamente.",
                details=str(e) if settings.debug else None
            ).model_dump()
        )

@app.get("/health", response_model=HealthResponse, summary="Health Check")
async def health_check_root():
    """Health check da API"""
    # Verificar se a API key do OpenAI está configurada
    if not settings.openai_api_key:
        return HealthResponse.create_warning(
            "API configurada, mas OPENAI_API_KEY não encontrada"
        )
    return HealthResponse.create_healthy()
