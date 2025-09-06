# AutoU Email Classifier

API para classificação automática de emails e geração de respostas usando IA.

## 🚀 Funcionalidades

- **Classificação**: Emails em "Produtivo" ou "Improdutivo"
- **Respostas Automáticas**: Baseadas na classificação
- **Suporte a Arquivos**: .txt e .pdf
- **API REST**: Interface simples

## 🛠️ Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar .env e adicionar sua chave OpenAI
OPENAI_API_KEY=sua_chave_aqui
```

### 3. Executar aplicação

```bash
# Iniciar API
python main.py

# Em outro terminal, iniciar frontend
cd frontend
python -m http.server 8001
```

- **API**: `http://localhost:8000`
- **Frontend**: `http://localhost:8001`

## 🌐 Interface Web

### Acessar a Interface

1. Inicie a API: `python main.py`
2. Inicie o frontend: `cd frontend && python -m http.server 8001`
3. Acesse: `http://localhost:8001`

### Funcionalidades da Interface

- ✅ **Upload de arquivos** (.txt, .pdf)
- ✅ **Inserção direta de texto**
- ✅ **Classificação automática**
- ✅ **Exibição de resultados**
- ✅ **Interface responsiva**
- ✅ **Validação de entrada**

## 📖 Uso da API

### Endpoints Disponíveis

- `GET /` - Status da API
- `GET /health` - Health check
- `GET /categories` - Categorias disponíveis
- `POST /classify-email` - Classificação principal (texto + arquivo)
- `POST /classify-text` - Classificação apenas de texto

### Exemplo de Uso

```bash
# Classificar texto
curl -X POST "http://localhost:8000/classify-text" \
  -F "text=Preciso de ajuda com minha conta"

# Classificar arquivo
curl -X POST "http://localhost:8000/classify-email" \
  -F "file=@email.txt"
```

### Resposta Esperada

```json
{
  "category": "produtivo",
  "suggested_response": "Obrigado pelo seu contato...",
  "processing_time": 1.234,
  "text_length": 67
}
```

## 🏗️ Estrutura do Projeto

```
projeto-autoU-backend/
├── main.py                 # Ponto de entrada
├── app/                    # Código principal
│   ├── controllers/       # Controllers (rotas)
│   ├── services/          # Services (lógica)
│   ├── models/            # Models (dados)
│   └── utils/             # Utils (configurações)
├── frontend/              # Interface web
│   ├── index.html         # Interface principal
│   ├── exemplo_email.txt  # Arquivo de exemplo
│   └── README.md          # Documentação do frontend
├── tests/                 # Testes
├── requirements.txt       # Dependências
├── env.example           # Exemplo de configuração
└── README.md             # Este arquivo
```

## 🚀 Deploy na Nuvem

### Opções Gratuitas Recomendadas

#### 1. Render (Recomendado) ⭐

**Vantagens:**
- ✅ Plano gratuito generoso
- ✅ Deploy automático via GitHub
- ✅ SSL automático
- ✅ Fácil configuração

**Passos:**
1. Acesse [render.com](https://render.com) e faça login
2. Clique em "New +" → "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `autou-email-classifier`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
5. Adicione a variável de ambiente:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `sua-api-key-aqui`
6. Clique em "Create Web Service"

#### 2. Railway

**Vantagens:**
- ✅ Interface moderna
- ✅ Deploy automático
- ✅ Suporte nativo ao Python

**Passos:**
1. Acesse [railway.app](https://railway.app) e faça login
2. Clique em "New Project" → "Deploy from GitHub repo"
3. Selecione seu repositório
4. Adicione a variável de ambiente `OPENAI_API_KEY`
5. Deploy automático

### Configuração da API Key

1. Acesse [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crie uma nova API key
3. Configure a variável de ambiente `OPENAI_API_KEY` na plataforma escolhida

### Verificação do Deploy

Após o deploy, teste:
- **Frontend**: `https://projeto-autou-1jup.onrender.com/`
- **API Health**: `https://projeto-autou-1jup.onrender.com/health`
- **Documentação**: `https://projeto-autou-1jup.onrender.com/docs`

### 🎉 Aplicação Deployada

**URL da Aplicação**: [https://projeto-autou-1jup.onrender.com/](https://projeto-autou-1jup.onrender.com/)

**Status**: ✅ Funcionando perfeitamente!

**Funcionalidades disponíveis**:
- ✅ Interface web responsiva
- ✅ Upload de arquivos (.txt, .pdf)
- ✅ Classificação de emails com IA
- ✅ Geração de respostas automáticas
- ✅ API REST completa

## 🧪 Testes

### Teste Local

```bash
# Executar testes
python tests/test_examples.py

# Limpar cache
python clean.py
```

### Teste da Aplicação Deployada

**1. Acesse a aplicação**: [https://projeto-autou-1jup.onrender.com/](https://projeto-autou-1jup.onrender.com/)

**2. Teste com email de exemplo**:
```
Assunto: Solicitação de suporte técnico

Olá equipe,

Estou enfrentando problemas para acessar minha conta no sistema. 
Podem me ajudar a resolver isso?

Obrigado,
João Silva
```

**3. Verifique os resultados**:
- ✅ Categoria: "Produtivo" ou "Improdutivo"
- ✅ Resposta sugerida pela IA
- ✅ Tempo de processamento
- ✅ Tamanho do texto

**4. Teste via API**:
```bash
curl -X POST "https://projeto-autou-1jup.onrender.com/classify-text" \
  -F "text=Preciso de ajuda com minha conta"
```

## 📄 Documentação

### Documentação Interativa da API

- **Local**: `http://localhost:8000/docs`
- **Produção**: [https://projeto-autou-1jup.onrender.com/docs](https://projeto-autou-1jup.onrender.com/docs)

### Endpoints Disponíveis

- `GET /` - Interface web principal
- `GET /health` - Health check da API
- `GET /categories` - Categorias disponíveis
- `POST /classify-email` - Classificação de email (arquivo + texto)
- `POST /classify-text` - Classificação apenas de texto

---

**Desenvolvido para o Case Prático AutoU** 🚀
