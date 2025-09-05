# Plano de Implementação - Backend AutoU (Case Prático)

## Visão Geral do Projeto

O projeto AutoU é um case prático que consiste em uma aplicação web simples que utiliza inteligência artificial para classificar emails em categorias (Produtivo/Improdutivo) e sugerir respostas automáticas.

## Requisitos Essenciais

### 1. Processamento de Emails

- **Leitura de arquivos**: Suporte para .txt e .pdf
- **Entrada de texto**: Aceitar texto direto via interface
- **Pré-processamento básico**: Limpeza simples do texto

### 2. Classificação de Emails

- **Categorias**: Produtivo vs Improdutivo
- **API de IA**: OpenAI GPT ou Hugging Face
- **Classificação funcional**: Básica mas efetiva

### 3. Geração de Respostas

- **Respostas automáticas**: Baseadas na classificação
- **Templates simples**: Respostas adequadas por categoria

### 4. API Simples

- **Endpoint único**: Para classificação e resposta
- **Upload de arquivos**: Processamento básico
- **Retorno JSON**: Resultado da classificação

## Arquitetura Simples

### Stack Tecnológica

- **Linguagem**: Python 3.9+
- **Framework Web**: FastAPI (simples e eficiente)
- **IA**: OpenAI API (GPT-3.5-turbo)
- **Processamento de PDF**: PyPDF2
- **Validação**: Pydantic

### Estrutura de Pastas Simplificada

```
backend/
├── main.py                    # Aplicação principal
├── email_classifier.py        # Lógica de classificação
├── file_processor.py          # Processamento de arquivos
├── requirements.txt           # Dependências
├── .env                      # Variáveis de ambiente
└── docs/
    └── plano_implementacao_backend.md
```

## Implementação Simplificada

### 1. Dependências (requirements.txt)

```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
openai==1.3.0
pypdf2==3.0.1
python-dotenv==1.0.0
```

### 2. Variáveis de Ambiente (.env)

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Modelos de Dados (main.py)

```python
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class EmailCategory(str, Enum):
    PRODUTIVO = "produtivo"
    IMPRODUTIVO = "improdutivo"

class EmailResponse(BaseModel):
    category: EmailCategory
    suggested_response: str
```

### 4. Funcionalidades Principais

#### 4.1 Processamento de Arquivos (file_processor.py)

```python
import PyPDF2
from io import BytesIO

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extrai texto de arquivo PDF"""
    pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def clean_text(text: str) -> str:
    """Limpa texto básico"""
    return text.strip().replace('\n', ' ')
```

#### 4.2 Classificação de Emails (email_classifier.py)

```python
import openai
from .models import EmailCategory

def classify_email(text: str) -> EmailCategory:
    """Classifica email usando OpenAI"""
    prompt = f"""
    Classifique o seguinte email como "produtivo" ou "improdutivo":

    Email: {text}

    Responda apenas com: produtivo ou improdutivo
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content.lower().strip()
    return EmailCategory.PRODUTIVO if "produtivo" in result else EmailCategory.IMPRODUTIVO

def generate_response(text: str, category: EmailCategory) -> str:
    """Gera resposta automática baseada na categoria"""
    if category == EmailCategory.PRODUTIVO:
        return "Obrigado pelo seu contato. Vamos analisar sua solicitação e retornaremos em breve."
    else:
        return "Obrigado pela sua mensagem. Agradecemos o contato."
```

### 5. API Principal (main.py)

```python
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from email_classifier import classify_email, generate_response
from file_processor import extract_text_from_pdf, clean_text
from models import EmailResponse, EmailCategory
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AutoU Email Classifier")

# CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/classify-email", response_model=EmailResponse)
async def classify_email_endpoint(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    """Classifica email e gera resposta automática"""

    # Processar entrada
    if file:
        if file.filename.endswith('.pdf'):
            content = await file.read()
            email_text = extract_text_from_pdf(content)
        elif file.filename.endswith('.txt'):
            content = await file.read()
            email_text = content.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Formato não suportado")
    elif text:
        email_text = text
    else:
        raise HTTPException(status_code=400, detail="Texto ou arquivo é obrigatório")

    # Limpar texto
    email_text = clean_text(email_text)

    # Classificar
    category = classify_email(email_text)

    # Gerar resposta
    suggested_response = generate_response(email_text, category)

    return EmailResponse(
        category=category,
        suggested_response=suggested_response
    )

@app.get("/")
async def root():
    return {"message": "AutoU Email Classifier API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Fluxo Simples

1. **Receber entrada**: Texto direto ou arquivo (.txt/.pdf)
2. **Processar**: Extrair e limpar texto
3. **Classificar**: Usar OpenAI para categorizar
4. **Gerar resposta**: Template baseado na categoria
5. **Retornar**: JSON com resultado

## Como Executar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

```bash
# Criar arquivo .env
echo "OPENAI_API_KEY=sua_chave_aqui" > .env
```

### 3. Executar aplicação

```bash
python main.py
```

### 4. Testar API

```bash
# Teste simples
curl -X POST "http://localhost:8000/classify-email" \
  -F "text=Preciso de ajuda com meu pedido"
```

## Deploy Simples

### Opção 1: Render (Recomendado)

1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Deploy automático

### Opção 2: Heroku

1. Criar Procfile: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Deploy via Git

### Opção 3: Railway

1. Conectar repositório
2. Configurar variáveis
3. Deploy automático

---

_Este plano serve como guia para a implementação do backend do projeto AutoU. Deve ser revisado e ajustado conforme necessário durante o desenvolvimento._
