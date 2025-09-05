"""
Script de exemplo para testar a API do AutoU Email Classifier
Execute este script para testar as funcionalidades da API
"""

import requests
import json
import time

# URL base da API
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Testa o health check da API"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando: {data['message']}")
            return True
        else:
            print(f"❌ Erro no health check: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se de que ela está rodando.")
        return False

def test_categories():
    """Testa o endpoint de categorias"""
    print("\n📋 Testando endpoint de categorias...")
    try:
        response = requests.get(f"{BASE_URL}/categories")
        if response.status_code == 200:
            data = response.json()
            print("✅ Categorias disponíveis:")
            for category in data['categories']:
                print(f"  - {category['name']}: {category['description']}")
            return True
        else:
            print(f"❌ Erro ao buscar categorias: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

def test_classify_text():
    """Testa a classificação de texto"""
    print("\n📧 Testando classificação de texto...")
    
    test_emails = [
        {
            "text": "Olá, preciso de ajuda com minha conta. Não consigo fazer login e preciso acessar meus dados urgentemente.",
            "expected": "produtivo"
        },
        {
            "text": "Feliz Natal! Desejo um ótimo fim de ano para toda a equipe.",
            "expected": "improdutivo"
        },
        {
            "text": "Gostaria de saber o status do meu pedido número 12345. Quando será entregue?",
            "expected": "produtivo"
        },
        {
            "text": "Obrigado pelo excelente atendimento! Vocês são demais!",
            "expected": "improdutivo"
        }
    ]
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n  Teste {i}: {email['text'][:50]}...")
        try:
            response = requests.post(
                f"{BASE_URL}/classify-text",
                data={"text": email["text"]}
            )
            
            if response.status_code == 200:
                data = response.json()
                category = data['category']
                response_text = data['suggested_response']
                processing_time = data['processing_time']
                
                status = "✅" if category == email['expected'] else "⚠️"
                print(f"    {status} Categoria: {category} (esperado: {email['expected']})")
                print(f"    📝 Resposta: {response_text}")
                print(f"    ⏱️  Tempo: {processing_time}s")
            else:
                print(f"    ❌ Erro: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"    ❌ Erro: {str(e)}")

def test_classify_file():
    """Testa a classificação de arquivo"""
    print("\n📁 Testando classificação de arquivo...")
    
    # Criar arquivo de teste
    test_content = "Preciso de suporte técnico urgente. Meu sistema não está funcionando corretamente."
    
    try:
        # Simular upload de arquivo
        files = {
            'file': ('test_email.txt', test_content, 'text/plain')
        }
        
        response = requests.post(
            f"{BASE_URL}/classify-email",
            files=files
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Arquivo classificado: {data['category']}")
            print(f"📝 Resposta: {data['suggested_response']}")
            print(f"⏱️  Tempo: {data['processing_time']}s")
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def test_error_handling():
    """Testa o tratamento de erros"""
    print("\n🚨 Testando tratamento de erros...")
    
    # Teste 1: Texto vazio
    print("  Teste 1: Texto vazio")
    try:
        response = requests.post(
            f"{BASE_URL}/classify-text",
            data={"text": ""}
        )
        if response.status_code == 400:
            print("    ✅ Erro tratado corretamente")
        else:
            print(f"    ❌ Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"    ❌ Erro: {str(e)}")
    
    # Teste 2: Texto muito curto
    print("  Teste 2: Texto muito curto")
    try:
        response = requests.post(
            f"{BASE_URL}/classify-text",
            data={"text": "Oi"}
        )
        if response.status_code == 400:
            print("    ✅ Erro tratado corretamente")
        else:
            print(f"    ❌ Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"    ❌ Erro: {str(e)}")

def main():
    """Função principal para executar todos os testes"""
    print("🚀 Iniciando testes da API AutoU Email Classifier")
    print("=" * 50)
    
    # Verificar se a API está rodando
    if not test_health_check():
        print("\n❌ API não está funcionando. Execute 'python main.py' primeiro.")
        return
    
    # Executar testes
    test_categories()
    test_classify_text()
    test_classify_file()
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")
    print("\n💡 Dicas:")
    print("  - Acesse http://localhost:8000/docs para documentação interativa")
    print("  - Configure OPENAI_API_KEY para melhor precisão na classificação")
    print("  - Use o endpoint /classify-email para upload de arquivos")

if __name__ == "__main__":
    main()
