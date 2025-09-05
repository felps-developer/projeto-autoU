"""
Serviço para classificação de emails e geração de respostas
"""

import openai
from typing import Tuple
from ..models.email_models import EmailCategory
from ..utils.config import settings


class EmailClassifier:
    """Classe para classificação de emails"""
    
    def __init__(self):
        """Inicializa o classificador"""
        self._setup_openai()
    
    def _setup_openai(self):
        """Configura a API do OpenAI"""
        if not settings.openai_api_key:
            print("⚠️  OPENAI_API_KEY não encontrada. Usando classificação por palavras-chave.")
            return
        
        openai.api_key = settings.openai_api_key
    
    def _get_classification_prompt(self, text: str) -> str:
        """
        Cria o prompt para classificação do email
        
        Args:
            text: Texto do email
            
        Returns:
            str: Prompt formatado para a API
        """
        prompt = f"""
Você é um assistente especializado em classificar emails para uma empresa financeira.

Classifique o seguinte email como "produtivo" ou "improdutivo":

PRODUTIVO: Emails que requerem uma ação ou resposta específica, como:
- Solicitações de suporte técnico
- Atualizações sobre casos em aberto
- Dúvidas sobre o sistema
- Reclamações ou problemas
- Solicitações de informações importantes

IMPRODUTIVO: Emails que não necessitam de uma ação imediata, como:
- Mensagens de felicitações (Natal, Ano Novo, etc.)
- Agradecimentos genéricos
- Mensagens de spam
- Conteúdo irrelevante

Email para classificar:
"{text}"

Responda APENAS com uma das palavras: "produtivo" ou "improdutivo"
"""
        return prompt
    
    def classify_email(self, text: str) -> EmailCategory:
        """
        Classifica um email usando OpenAI GPT
        
        Args:
            text: Texto do email para classificar
            
        Returns:
            EmailCategory: Categoria do email (PRODUTIVO ou IMPRODUTIVO)
        """
        try:
            if not settings.openai_api_key:
                return self._classify_by_keywords(text)
            
            # Criar prompt
            prompt = self._get_classification_prompt(text)
            
            # Chamar API do OpenAI
            response = openai.ChatCompletion.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "Você é um classificador de emails especializado."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=settings.openai_temperature
            )
            
            # Extrair resultado
            result = response.choices[0].message.content.lower().strip()
            
            # Validar e retornar categoria
            if "produtivo" in result:
                return EmailCategory.PRODUTIVO
            elif "improdutivo" in result:
                return EmailCategory.IMPRODUTIVO
            else:
                # Fallback: tentar classificar baseado em palavras-chave
                return self._classify_by_keywords(text)
        
        except Exception as e:
            print(f"Erro na classificação com OpenAI: {str(e)}")
            # Fallback para classificação por palavras-chave
            return self._classify_by_keywords(text)
    
    def _classify_by_keywords(self, text: str) -> EmailCategory:
        """
        Classificação de fallback baseada em palavras-chave
        
        Args:
            text: Texto do email
            
        Returns:
            EmailCategory: Categoria baseada em palavras-chave
        """
        text_lower = text.lower()
        
        # Palavras-chave para emails produtivos
        produtivo_keywords = [
            "problema", "erro", "bug", "não funciona", "ajuda", "suporte",
            "solicitação", "pedido", "reclamação", "dúvida", "questão",
            "atualização", "status", "andamento", "prazo", "urgente",
            "sistema", "conta", "pagamento", "fatura", "cobrança"
        ]
        
        # Palavras-chave para emails improdutivos
        improdutivo_keywords = [
            "feliz natal", "feliz ano novo", "parabéns", "obrigado",
            "agradecimento", "spam", "promoção", "oferta", "desconto"
        ]
        
        # Contar ocorrências
        produtivo_count = sum(1 for keyword in produtivo_keywords if keyword in text_lower)
        improdutivo_count = sum(1 for keyword in improdutivo_keywords if keyword in text_lower)
        
        # Retornar categoria baseada na contagem
        if produtivo_count > improdutivo_count:
            return EmailCategory.PRODUTIVO
        else:
            return EmailCategory.IMPRODUTIVO
    
    def _get_response_prompt(self, text: str, category: EmailCategory) -> str:
        """
        Cria o prompt para geração de resposta baseada na categoria
        
        Args:
            text: Texto do email original
            category: Categoria do email
            
        Returns:
            str: Prompt para geração de resposta
        """
        if category == EmailCategory.PRODUTIVO:
            prompt = f"""
Você é um assistente de atendimento de uma empresa financeira.

Um cliente enviou o seguinte email que foi classificado como PRODUTIVO (requer ação):

"{text}"

Gere uma resposta profissional e útil que:
1. Agradeça o contato
2. Confirme que a solicitação será analisada
3. Informe que retornará em breve
4. Seja cordial e profissional

Mantenha a resposta concisa (máximo 3 linhas).
"""
        else:
            prompt = f"""
Você é um assistente de atendimento de uma empresa financeira.

Um cliente enviou o seguinte email que foi classificado como IMPRODUTIVO (não requer ação):

"{text}"

Gere uma resposta educada e cordial que:
1. Agradeça a mensagem
2. Seja breve e amigável
3. Mantenha o tom profissional

Mantenha a resposta muito concisa (máximo 2 linhas).
"""
        
        return prompt
    
    def generate_response(self, text: str, category: EmailCategory) -> str:
        """
        Gera uma resposta automática baseada na categoria do email
        
        Args:
            text: Texto do email original
            category: Categoria do email
            
        Returns:
            str: Resposta automática gerada
        """
        try:
            if not settings.openai_api_key:
                return self._get_template_response(category)
            
            # Criar prompt
            prompt = self._get_response_prompt(text, category)
            
            # Chamar API do OpenAI
            response = openai.ChatCompletion.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "Você é um assistente de atendimento profissional."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.openai_max_tokens,
                temperature=0.7
            )
            
            # Extrair resposta
            generated_response = response.choices[0].message.content.strip()
            
            return generated_response
        
        except Exception as e:
            print(f"Erro na geração de resposta: {str(e)}")
            # Fallback para respostas template
            return self._get_template_response(category)
    
    def _get_template_response(self, category: EmailCategory) -> str:
        """
        Respostas template de fallback
        
        Args:
            category: Categoria do email
            
        Returns:
            str: Resposta template
        """
        if category == EmailCategory.PRODUTIVO:
            return "Obrigado pelo seu contato. Recebemos sua solicitação e nossa equipe irá analisá-la em breve. Retornaremos com uma resposta o mais rápido possível."
        else:
            return "Obrigado pela sua mensagem. Agradecemos o contato e desejamos um ótimo dia!"
    
    def classify_and_generate_response(self, text: str) -> Tuple[EmailCategory, str]:
        """
        Classifica o email e gera uma resposta automática
        
        Args:
            text: Texto do email
            
        Returns:
            Tuple[EmailCategory, str]: Categoria e resposta gerada
        """
        # Classificar email
        category = self.classify_email(text)
        
        # Gerar resposta
        response = self.generate_response(text, category)
        
        return category, response
