# 🚀 Deploy do AutoU Email Classifier

Este guia explica como fazer deploy da aplicação AutoU Email Classifier em plataformas de nuvem gratuitas.

## 📋 Pré-requisitos

1. **Conta OpenAI**: Você precisa de uma API key da OpenAI para usar o GPT-3.5-turbo
2. **Repositório GitHub**: O código deve estar em um repositório público no GitHub
3. **Conta na plataforma de deploy**: Render, Railway, ou Heroku

## 🔑 Configuração da API Key

Antes do deploy, você precisa configurar a variável de ambiente `OPENAI_API_KEY`:

1. Acesse [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crie uma nova API key
3. Copie a chave (ela começa com `sk-`)

## 🌐 Opções de Deploy

### 1. Render (Recomendado)

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

### 2. Railway

**Vantagens:**
- ✅ Interface moderna
- ✅ Deploy automático
- ✅ Suporte nativo ao Python

**Passos:**

1. Acesse [railway.app](https://railway.app) e faça login
2. Clique em "New Project" → "Deploy from GitHub repo"
3. Selecione seu repositório
4. Railway detectará automaticamente que é um projeto Python
5. Adicione a variável de ambiente:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `sua-api-key-aqui`
6. O deploy será automático

### 3. Heroku

**Vantagens:**
- ✅ Plataforma clássica
- ✅ Boa documentação

**Limitações:**
- ⚠️ Plano gratuito foi descontinuado
- ⚠️ Requer cartão de crédito para planos pagos

**Passos (se usar plano pago):**

1. Instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Faça login: `heroku login`
3. Crie a aplicação: `heroku create autou-email-classifier`
4. Configure a API key: `heroku config:set OPENAI_API_KEY=sua-api-key-aqui`
5. Faça o deploy: `git push heroku main`

## 🔧 Configurações Adicionais

### Variáveis de Ambiente Recomendadas

```bash
OPENAI_API_KEY=sk-sua-chave-aqui
DEBUG=false
CORS_ORIGINS=*
```

### Verificação do Deploy

Após o deploy, teste os seguintes endpoints:

- **Frontend**: `https://sua-app.onrender.com/`
- **API Health**: `https://sua-app.onrender.com/health`
- **Documentação**: `https://sua-app.onrender.com/docs`

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro 500 na API**
   - Verifique se a `OPENAI_API_KEY` está configurada
   - Verifique os logs da aplicação

2. **Frontend não carrega**
   - Verifique se o arquivo `frontend/index.html` existe
   - Verifique se a rota `/` está funcionando

3. **CORS Error**
   - Verifique se `CORS_ORIGINS=*` está configurado
   - Verifique se o frontend está usando a URL correta da API

### Logs

Para ver os logs da aplicação:

- **Render**: Dashboard → Logs
- **Railway**: Deploy → View Logs
- **Heroku**: `heroku logs --tail`

## 📱 Testando a Aplicação

1. Acesse a URL da aplicação
2. Teste com um email de exemplo:

```
Assunto: Solicitação de suporte técnico

Olá equipe,

Estou enfrentando problemas para acessar minha conta no sistema. 
Podem me ajudar a resolver isso?

Obrigado,
João Silva
```

3. Verifique se a classificação e resposta sugerida aparecem corretamente

## 🎯 Próximos Passos

Após o deploy bem-sucedido:

1. ✅ Teste todas as funcionalidades
2. ✅ Grave o vídeo demonstrativo
3. ✅ Prepare o README do repositório
4. ✅ Submeta o projeto no formulário da AutoU

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs da aplicação
2. Teste localmente primeiro
3. Verifique se todas as dependências estão no `requirements.txt`
4. Confirme se a API key da OpenAI está válida

---

**Boa sorte com o deploy! 🚀**
