#!/usr/bin/env python3
"""
Script para testar a aplicação antes do deploy
"""

import os
import sys
import requests
import time
from pathlib import Path

def test_local_app():
    """Testa a aplicação localmente"""
    print("🧪 Testando aplicação localmente...")
    
    # Verificar se a API está rodando
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API está rodando")
            health_data = response.json()
            print(f"   Status: {health_data.get('status', 'unknown')}")
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        print("   Certifique-se de que a API está rodando: python main.py")
        return False
    
    # Testar classificação de texto
    try:
        test_text = "Preciso de ajuda com minha conta no sistema."
        response = requests.post(
            "http://localhost:8000/classify-text",
            data={"text": test_text},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Classificação de texto funcionando")
            data = response.json()
            print(f"   Categoria: {data.get('category', 'unknown')}")
            print(f"   Tempo: {data.get('processing_time', 0):.2f}s")
        else:
            print(f"❌ Erro na classificação: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao testar classificação: {e}")
        return False
    
    # Verificar se o frontend existe
    frontend_path = Path("frontend/index.html")
    if frontend_path.exists():
        print("✅ Frontend encontrado")
    else:
        print("❌ Frontend não encontrado")
        return False
    
    print("\n🎉 Todos os testes passaram! A aplicação está pronta para deploy.")
    return True

def check_requirements():
    """Verifica se todos os arquivos necessários existem"""
    print("📋 Verificando arquivos necessários...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "Procfile",
        "app/main.py",
        "frontend/index.html",
        "env.example"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Arquivos faltando:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Todos os arquivos necessários estão presentes")
    return True

def check_env_config():
    """Verifica configuração de ambiente"""
    print("🔧 Verificando configuração...")
    
    # Verificar se .env existe ou se as variáveis estão configuradas
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Arquivo .env encontrado")
    else:
        print("⚠️  Arquivo .env não encontrado")
        print("   Certifique-se de configurar OPENAI_API_KEY no deploy")
    
    # Verificar requirements.txt
    if Path("requirements.txt").exists():
        with open("requirements.txt", "r") as f:
            content = f.read()
            if "openai" in content and "fastapi" in content:
                print("✅ requirements.txt parece correto")
            else:
                print("❌ requirements.txt pode estar incompleto")
                return False
    
    return True

def main():
    """Função principal"""
    print("🚀 Teste de Deploy - AutoU Email Classifier")
    print("=" * 50)
    
    # Verificar arquivos
    if not check_requirements():
        print("\n❌ Falha na verificação de arquivos")
        sys.exit(1)
    
    # Verificar configuração
    if not check_env_config():
        print("\n❌ Falha na verificação de configuração")
        sys.exit(1)
    
    # Testar aplicação (opcional)
    print("\n" + "=" * 50)
    test_choice = input("Deseja testar a aplicação localmente? (s/n): ").lower().strip()
    
    if test_choice in ['s', 'sim', 'y', 'yes']:
        if not test_local_app():
            print("\n❌ Testes falharam")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎯 Próximos passos para deploy:")
    print("1. Faça commit e push do código para GitHub")
    print("2. Acesse render.com ou railway.app")
    print("3. Conecte seu repositório")
    print("4. Configure OPENAI_API_KEY")
    print("5. Faça o deploy!")
    print("\n📖 Veja DEPLOY.md para instruções detalhadas")

if __name__ == "__main__":
    main()
