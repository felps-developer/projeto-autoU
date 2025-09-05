"""
Ponto de entrada principal da aplicação AutoU Email Classifier
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando AutoU Email Classifier API...")
    print("📖 Documentação disponível em: http://localhost:8000/docs")
    print("🔍 Health check em: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
