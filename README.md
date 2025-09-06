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

## 🚀 Deploy

### Heroku

1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Deploy automático

### Render

1. Conectar repositório
2. Configurar variáveis
3. Deploy automático

## 🧪 Testes

```bash
# Executar testes
python tests/test_examples.py

# Limpar cache
python clean.py
```

## 📄 Documentação

Acesse `http://localhost:8000/docs` para documentação interativa da API.

---

**Desenvolvido para o Case Prático AutoU** 🚀
