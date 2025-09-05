"""
Serviço para classificação de emails e geração de respostas
"""

from openai import OpenAI
from typing import Tuple
from ..models.email_models import EmailCategory
from ..utils.config import settings


class EmailClassifier:
    """Classe para classificação de emails"""
    
    def __init__(self):
        """Inicializa o classificador"""
        if settings.openai_api_key:
            try:
                self.client = OpenAI(api_key=settings.openai_api_key)
            except Exception as e:
                print(f"⚠️  Erro ao inicializar OpenAI: {str(e)}")
                self.client = None
        else:
            self.client = None
            print("⚠️  OPENAI_API_KEY não encontrada. Usando classificação por palavras-chave.")
    
    def classify_email(self, text: str) -> EmailCategory:
        """Classifica um email"""
        try:
            if not self.client:
                return self._classify_by_keywords(text)
            
            prompt = f"""
Classifique o seguinte email como "produtivo" ou "improdutivo":

PRODUTIVO: Emails que requerem ação (suporte, dúvidas, problemas, solicitações)
IMPRODUTIVO: Emails que não requerem ação (felicitações, agradecimentos, spam)

Email: "{text}"

Responda APENAS: produtivo ou improdutivo
"""
            
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )
            
            result = response.choices[0].message.content.lower().strip()
            return EmailCategory.PRODUTIVO if "produtivo" in result else EmailCategory.IMPRODUTIVO
        
        except Exception as e:
            print(f"Erro na classificação: {str(e)}")
            return self._classify_by_keywords(text)
    
    def _classify_by_keywords(self, text: str) -> EmailCategory:
        """Classificação por palavras-chave"""
        text_lower = text.lower()
        
        produtivo_keywords = [
            "problema", "erro", "bug", "não funciona", "ajuda", "suporte",
            "solicitação", "pedido", "reclamação", "dúvida", "questão",
            "atualização", "status", "andamento", "prazo", "urgente"
        ]
        
        improdutivo_keywords = [
            "feliz natal", "feliz ano novo", "parabéns", "obrigado",
            "agradecimento", "spam", "promoção", "oferta"
        ]
        
        produtivo_count = sum(1 for keyword in produtivo_keywords if keyword in text_lower)
        improdutivo_count = sum(1 for keyword in improdutivo_keywords if keyword in text_lower)
        
        return EmailCategory.PRODUTIVO if produtivo_count > improdutivo_count else EmailCategory.IMPRODUTIVO
    
    def generate_response(self, text: str, category: EmailCategory) -> str:
        """Gera resposta automática"""
        try:
            if not self.client:
                return self._get_template_response(category)
            
            if category == EmailCategory.PRODUTIVO:
                prompt = f"Gere uma resposta profissional para este email produtivo: '{text}'. Seja conciso (máximo 3 linhas)."
            else:
                prompt = f"Gere uma resposta educada para este email improdutivo: '{text}'. Seja breve (máximo 2 linhas)."
            
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Erro na geração: {str(e)}")
            return self._get_template_response(category)
    
    def _get_template_response(self, category: EmailCategory) -> str:
        """Respostas template"""
        if category == EmailCategory.PRODUTIVO:
            return "Obrigado pelo seu contato. Recebemos sua solicitação e nossa equipe irá analisá-la em breve. Retornaremos com uma resposta o mais rápido possível."
        else:
            return "Obrigado pela sua mensagem. Agradecemos o contato e desejamos um ótimo dia!"
    
    def classify_and_generate_response(self, text: str) -> Tuple[EmailCategory, str]:
        """Classifica email e gera resposta"""
        category = self.classify_email(text)
        response = self.generate_response(text, category)
        return category, response