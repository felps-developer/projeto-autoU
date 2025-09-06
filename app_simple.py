"""
Aplicação principal AutoU Email Classifier - Versão para Deploy
"""

from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import time
import os
import json

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

@app.get("/categories")
async def get_categories():
    """Retorna as categorias disponíveis"""
    return {
        "categories": [
            {"id": "produtivo", "name": "Produtivo", "description": "Emails que requerem ação"},
            {"id": "improdutivo", "name": "Improdutivo", "description": "Emails que não requerem ação"}
        ]
    }

@app.post("/classify-text")
async def classify_text(text: str = Form(...)):
    """Classifica texto de email"""
    try:
        # Simulação de classificação (sem IA por enquanto)
        start_time = time.time()
        
        # Lógica simples de classificação baseada em palavras-chave
        text_lower = text.lower()
        
        # Palavras que indicam email produtivo
        productive_keywords = [
            "ajuda", "suporte", "problema", "erro", "bug", "conta", "login",
            "solicitação", "pedido", "urgente", "importante", "necessito",
            "preciso", "como", "quando", "onde", "por que", "dúvida"
        ]
        
        # Palavras que indicam email improdutivo
        unproductive_keywords = [
            "obrigado", "obrigada", "parabéns", "feliz", "natal", "ano novo",
            "cumprimentos", "saudações", "atenciosamente", "abraço", "beijo"
        ]
        
        productive_score = sum(1 for keyword in productive_keywords if keyword in text_lower)
        unproductive_score = sum(1 for keyword in unproductive_keywords if keyword in text_lower)
        
        if productive_score > unproductive_score:
            category = "produtivo"
            suggested_response = "Obrigado pelo seu contato. Nossa equipe analisará sua solicitação e retornará em breve."
        else:
            category = "improdutivo"
            suggested_response = "Obrigado pela sua mensagem. Agradecemos o contato!"
        
        processing_time = time.time() - start_time
        
        return {
            "category": category,
            "suggested_response": suggested_response,
            "processing_time": round(processing_time, 3),
            "text_length": len(text),
            "confidence": 0.8
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro na classificação: {str(e)}"}
        )

@app.post("/classify-email")
async def classify_email(
    file: UploadFile = File(None),
    text: str = Form(None)
):
    """Classifica email (arquivo ou texto)"""
    try:
        content = ""
        
        if file:
            # Processar arquivo
            if file.filename.endswith('.txt'):
                content = (await file.read()).decode('utf-8')
            else:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Apenas arquivos .txt são suportados nesta versão"}
                )
        elif text:
            content = text
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "É necessário fornecer um arquivo ou texto"}
            )
        
        if not content.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Conteúdo vazio"}
            )
        
        # Usar a mesma lógica de classificação
        result = await classify_text(content)
        return result
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro no processamento: {str(e)}"}
        )

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
