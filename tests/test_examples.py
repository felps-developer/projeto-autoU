"""
Script simples para testar a API
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa o health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API funcionando!")
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            return False
    except:
        print("❌ API não está rodando")
        return False

def test_classify():
    """Testa classificação de email"""
    print("\n📧 Testando classificação...")
    
    test_emails = [
        "Preciso de ajuda com minha conta. Não consigo fazer login.",
        "Feliz Natal! Desejo um ótimo fim de ano.",
        "Gostaria de saber o status do meu pedido número 12345."
    ]
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n  Teste {i}: {email[:50]}...")
        try:
            response = requests.post(
                f"{BASE_URL}/classify-text",
                data={"text": email}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"    ✅ Categoria: {data['category']}")
                print(f"    📝 Resposta: {data['suggested_response']}")
            else:
                print(f"    ❌ Erro: {response.status_code}")
                
        except Exception as e:
            print(f"    ❌ Erro: {str(e)}")

def main():
    """Função principal"""
    print("🚀 Testando AutoU Email Classifier API")
    print("=" * 40)
    
    if test_health():
        test_classify()
    
    print("\n" + "=" * 40)
    print("✅ Testes concluídos!")

if __name__ == "__main__":
    main()