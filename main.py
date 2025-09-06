"""
Ponto de entrada principal da aplicação AutoU Email Classifier
"""

from app.main import app

# Para compatibilidade com Render
if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    
    print("🚀 Iniciando AutoU Email Classifier API...")
    print("📖 Documentação disponível em: http://localhost:8000/docs")
    print("🔍 Health check em: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
