# Frontend - AutoU Email Classifier

Interface web simples e intuitiva para classificação de emails.

## 🚀 Como Usar

### 1. Iniciar o Backend

```bash
# Na pasta raiz do projeto
python main.py
```

### 2. Abrir a Interface

Abra o arquivo `index.html` no seu navegador ou use um servidor local:

```bash
# Usando Python (na pasta frontend)
python -m http.server 8001

# Acesse: http://localhost:8001
```

### 3. Testar a Aplicação

- **Upload de arquivo**: Selecione um arquivo .txt ou .pdf
- **Texto direto**: Digite ou cole o texto do email
- **Clique em "Classificar Email"**

## 📁 Arquivos

- `index.html` - Interface principal
- `exemplo_email.txt` - Arquivo de exemplo para teste
- `README.md` - Este arquivo

## ✨ Funcionalidades

- ✅ Upload de arquivos (.txt, .pdf)
- ✅ Inserção direta de texto
- ✅ Classificação automática
- ✅ Exibição de resultados
- ✅ Interface responsiva
- ✅ Validação de entrada
- ✅ Feedback visual

## 🎨 Características da Interface

- **Design moderno** com gradientes e sombras
- **Responsiva** para mobile e desktop
- **Intuitiva** sem necessidade de instruções
- **Feedback visual** com loading e resultados
- **Validação** de arquivos e texto
- **Organização clara** dos resultados

## 🔧 Configuração

A interface está configurada para conectar com a API em `http://localhost:8000`.

Para alterar a URL da API, edite a variável `API_BASE_URL` no JavaScript:

```javascript
const API_BASE_URL = "http://localhost:8000";
```

## 📱 Compatibilidade

- ✅ Chrome, Firefox, Safari, Edge
- ✅ Mobile e Desktop
- ✅ Windows, Mac, Linux
