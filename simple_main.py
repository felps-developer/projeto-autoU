"""
Versão simplificada para teste de deploy
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# Criar aplicação FastAPI
app = FastAPI(
    title="AutoU Email Classifier",
    description="API para classificação de emails e geração de respostas automáticas",
    version="1.0.0"
)

# CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Página inicial"""
    return {"message": "AutoU Email Classifier API está funcionando! 🚀"}

@app.get("/health")
async def health_check():
    """Health check da API"""
    return {
        "status": "healthy",
        "message": "API funcionando corretamente",
        "version": "1.0.0"
    }

@app.get("/docs")
async def docs():
    """Redirecionar para documentação"""
    return {"message": "Acesse /docs para ver a documentação da API"}

# Servir frontend se existir
@app.get("/frontend")
async def serve_frontend():
    """Serve o frontend da aplicação"""
    frontend_file = os.path.join("frontend", "index.html")
    if os.path.exists(frontend_file):
        return FileResponse(frontend_file)
    return {"message": "Frontend não encontrado"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
