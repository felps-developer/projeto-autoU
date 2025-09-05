# AutoU Email Classifier - Backend

API para classificação automática de emails e geração de respostas usando inteligência artificial.

## 🚀 Funcionalidades

- **Classificação de Emails**: Categoriza emails em "Produtivo" ou "Improdutivo"
- **Geração de Respostas**: Cria respostas automáticas baseadas na classificação
- **Suporte a Arquivos**: Processa arquivos .txt e .pdf
- **API REST**: Interface simples e documentada
- **Fallback Inteligente**: Sistema de backup quando a API do OpenAI não está disponível

## 📋 Requisitos

- Python 3.9+
- Chave da API do OpenAI (opcional, mas recomendada)

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd projeto-autoU-backend
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env e adicione sua chave da OpenAI
OPENAI_API_KEY=sua_chave_aqui
```

### 4. Execute a aplicação

```bash
python main.py
```

### 5. Limpar cache (opcional)

```bash
python clean.py
```

A API estará disponível em: `http://localhost:8000`

## 📖 Documentação da API

### Endpoints Disponíveis

#### `GET /`

- **Descrição**: Endpoint raiz
- **Resposta**: Status da API

#### `GET /health`

- **Descrição**: Health check da API
- **Resposta**: Status detalhado da aplicação

#### `GET /categories`

- **Descrição**: Lista as categorias de classificação
- **Resposta**: Categorias disponíveis com exemplos

#### `POST /classify-email`

- **Descrição**: Classifica email e gera resposta automática
- **Parâmetros**:
  - `text` (opcional): Texto do email
  - `file` (opcional): Arquivo .txt ou .pdf
- **Resposta**: Categoria e resposta sugerida

#### `POST /classify-text`

- **Descrição**: Classifica apenas texto (endpoint simplificado)
- **Parâmetros**:
  - `text` (obrigatório): Texto do email
- **Resposta**: Categoria e resposta sugerida

### Exemplo de Uso

#### Classificar texto direto:

```bash
curl -X POST "http://localhost:8000/classify-email" \
  -F "text=Preciso de ajuda com meu pedido, não consigo acessar minha conta"
```

#### Classificar arquivo:

```bash
curl -X POST "http://localhost:8000/classify-email" \
  -F "file=@email.txt"
```

#### Resposta esperada:

```json
{
  "category": "produtivo",
  "suggested_response": "Obrigado pelo seu contato. Recebemos sua solicitação e nossa equipe irá analisá-la em breve. Retornaremos com uma resposta o mais rápido possível.",
  "processing_time": 1.234,
  "text_length": 67
}
```

## 🔧 Configuração

### Variáveis de Ambiente

| Variável         | Descrição              | Obrigatória |
| ---------------- | ---------------------- | ----------- |
| `OPENAI_API_KEY` | Chave da API do OpenAI | Não\*       |

\*Sem a chave da OpenAI, o sistema usará classificação por palavras-chave como fallback.

### Obter Chave da OpenAI

1. Acesse [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crie uma conta ou faça login
3. Gere uma nova API key
4. Adicione no arquivo `.env`

## 🏗️ Arquitetura MVC

O projeto segue o padrão **Model-View-Controller (MVC)**:

- **Controllers** (`app/controllers/`): Rotas finais da API, recebem requisições e retornam respostas
- **Services** (`app/services/`): Lógica de negócio, processamento e regras da aplicação
- **Models** (`app/models/`): Modelos de dados, estruturas e validações
- **Utils** (`app/utils/`): Funções auxiliares e configurações

## 🏗️ Estrutura do Projeto

```
projeto-autoU-backend/
├── main.py                 # Ponto de entrada da aplicação
├── app/                    # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py            # Aplicação FastAPI
│   ├── controllers/       # Controllers (rotas finais)
│   │   ├── __init__.py
│   │   └── email_controller.py
│   ├── services/          # Services (lógica de negócio)
│   │   ├── __init__.py
│   │   ├── email_classifier.py
│   │   └── file_processor.py
│   ├── models/            # Models (modelos de dados)
│   │   ├── __init__.py
│   │   └── email_models.py
│   └── utils/             # Utils (funções e configurações)
│       ├── __init__.py
│       └── config.py
├── tests/                 # Testes
│   ├── __init__.py
│   └── test_examples.py
├── docs/                  # Documentação
│   └── plano_implementacao_backend.md
├── requirements.txt       # Dependências Python
├── env.example           # Exemplo de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── Procfile              # Para deploy no Heroku
├── runtime.txt           # Versão do Python para Heroku
├── clean.py              # Script para limpar cache Python
└── README.md             # Este arquivo
```

## 🚀 Deploy

### Render (Recomendado)

1. Conecte seu repositório GitHub ao Render
2. Configure as variáveis de ambiente
3. Deploy automático

### Heroku

1. Crie um `Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Deploy via Git:

```bash
git push heroku main
```

### Railway

1. Conecte o repositório
2. Configure as variáveis de ambiente
3. Deploy automático

## 🧪 Testando a API

### Usando curl

```bash
# Health check
curl http://localhost:8000/health

# Classificar texto
curl -X POST "http://localhost:8000/classify-email" \
  -F "text=Olá, preciso de ajuda com minha conta"

# Ver categorias
curl http://localhost:8000/categories
```

### Usando a documentação interativa

Acesse `http://localhost:8000/docs` para testar a API diretamente no navegador.

## 🔍 Categorias de Classificação

### Produtivo

Emails que requerem uma ação ou resposta específica:

- Solicitações de suporte técnico
- Atualizações sobre casos em aberto
- Dúvidas sobre o sistema
- Reclamações ou problemas

### Improdutivo

Emails que não necessitam de uma ação imediata:

- Mensagens de felicitações
- Agradecimentos genéricos
- Mensagens de spam
- Conteúdo irrelevante

## 🛡️ Tratamento de Erros

A API inclui tratamento robusto de erros:

- **400 Bad Request**: Entrada inválida
- **413 Payload Too Large**: Arquivo muito grande
- **500 Internal Server Error**: Erro interno

## 📊 Monitoramento

A API inclui:

- Logging de requisições
- Tempo de processamento
- Health checks
- Tratamento de erros

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é parte do case prático da AutoU.

## 🆘 Suporte

Para dúvidas ou problemas:

1. Verifique a documentação da API em `/docs`
2. Consulte os logs da aplicação
3. Verifique se a chave da OpenAI está configurada corretamente

---

**Desenvolvido para o Case Prático AutoU** 🚀
