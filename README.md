# Bot YouTube Shorts Automático - 100% GRATUITO

Bot que gera e posta YouTube Shorts automaticamente usando **APENAS serviços gratuitos**.

## 🎉 **ZERO CUSTOS - TOTALMENTE GRATUITO!**

- ✅ **Grok (xAI)**: 100% gratuito, sem limites
- ✅ **Vídeos Pexels**: 200 requests/hora gratuito
- ✅ **YouTube Upload**: Gratuito
- ✅ **Gemini (Google)**: Gratuito quando disponível

**Total: $0.00** - Sem custos ocultos!

## 🚀 Como Usar (3 Passos Simples)

### 1. **Instalar**
```bash
git clone <seu-repo>
cd Bot_Youtube
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. **Configurar Chaves Gratuitas**
```bash
cp .env.example .env
```

Edite `.env` com apenas 2 chaves gratuitas:
```env
GROQ_API_KEY=gsk_...  # Groq Console: https://console.groq.com/keys
PEXELS_API_KEY=...    # Pexels: https://www.pexels.com/api/
```

### 3. **Executar**
```bash
python bot_youtube.py
```

**Pronto!** O bot gera vídeos automaticamente sem custos!

## 🚀 Funcionalidades

- Geração automática de roteiro com Gemini AI
- Síntese de voz em português brasileiro
- Download de vídeos de fundo do Pexels
- Edição automática de vídeo
- Upload direto para YouTube

## 📋 Pré-requisitos

- Python 3.8+
- Conta Google Cloud com YouTube Data API v3 habilitada
- Chave API Gemini (Google AI Studio)
- Chave API Pexels

## 🛠️ Instalação

1. **Clone o repositório:**
   ```bash
   git clone <seu-repo>
   cd Bot_Youtube
   ```

2. **Configure o ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou .venv\Scripts\activate no Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as APIs:**
   - Edite o arquivo `.env` com suas chaves API
   - Baixe o `credentials.json` do Google Cloud Console

## ⚙️ Configuração

### Arquivo .env
Copie o arquivo `.env.example` para `.env` e configure suas chaves:

```bash
cp .env.example .env
# Edite o .env com suas chaves reais
```

```env
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
GEMINI_API_KEY=sua_chave_gemini_aqui
PEXELS_API_KEY=sua_chave_pexels_aqui
```

### APIs de IA (Escolha uma ou mais):

### APIs de IA (Escolha uma ou mais):

#### 1. **Grok (xAI) - 100% GRATUITO! ⭐⭐⭐⭐⭐**
- **Por que é melhor:** Completamente gratuito, sem limites conhecidos
- **Criado por:** xAI (Elon Musk)
- **Como obter:** [Groq Console](https://console.groq.com/keys)
- **Modelo:** grok-beta

#### 2. **Gemini (Google) - Gratuito limitado**
- **Quotas:** Reseta diariamente
- **Como obter:** [Google AI Studio](https://aistudio.google.com/app/apikey)

#### 3. **Claude (Anthropic) - $5/mês gratuito**
- **Tier gratuito:** 5$ de créditos por mês
- **Como obter:** [Anthropic Console](https://console.anthropic.com/)

#### 4. **OpenAI GPT - Pago**
- **Como obter:** [OpenAI Platform](https://platform.openai.com/api-keys)

### Google Cloud Console
1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto ou selecione existente
3. Habilite a YouTube Data API v3
4. Crie credenciais OAuth 2.0
5. Baixe o `credentials.json` e coloque na raiz do projeto

## ▶️ Como Usar

1. **Ative o ambiente virtual:**
   ```bash
   source .venv/bin/activate
   ```

2. **Execute o bot:**
   ```bash
   python bot_youtube.py
   ```

3. **Primeira execução:**
   - O navegador abrirá para autenticação OAuth
   - Autorize as permissões do YouTube
   - O `token.json` será criado automaticamente

## 🔧 Tratamento de Erros

### Quota Excedida (429)
- O bot automaticamente aguarda o tempo sugerido pela API
- Máximo de 3 tentativas por operação
- Considere fazer upgrade para plano pago do Gemini

### Outros Erros
- Verifique se todas as dependências estão instaladas
- Confirme que as chaves API são válidas
- Certifique-se de que `credentials.json` tem permissões corretas

## 📁 Estrutura do Projeto

```
Bot_Youtube/
├── bot_youtube.py          # Script principal
├── credentials.json        # Credenciais Google (não versionar)
├── token.json             # Token OAuth (gerado automaticamente)
├── .env                   # Chaves API (não versionar)
├── requirements.txt       # Dependências Python
├── README.md              # Este arquivo
└── .venv/                 # Ambiente virtual (não versionar)
```

## 🔒 Segurança

- Nunca commite arquivos com chaves API (`credentials.json`, `.env`)
- Use variáveis de ambiente para produção
- Mantenha o ambiente virtual isolado

## 🤖 Modelos de IA

O bot tenta os modelos na seguinte ordem de prioridade (gratuitos primeiro):

1. **Grok (xAI)** ⭐⭐⭐⭐⭐ - **100% GRATUITO** (Sem limites conhecidos)
2. **Gemini (Google)** - Gratuito limitado (reseta diariamente)
3. **Claude (Anthropic)** - $5/mês de créditos gratuitos
4. **GPT-3.5 Turbo** - Pago ($0.002/1K tokens)
5. **GPT-4** - Pago ($0.03/1K input)

**O bot automaticamente pula para o próximo modelo se um falhar por quota.**

### 💰 Custos por Vídeo (Opções Gratuitas):

| Modelo | Custo | Status |
|--------|-------|--------|
| **Grok** | $0.00 🎉 | 100% Gratuito |
| **Gemini** | $0.00 (limitado) | Gratuito quando disponível |
| **Vídeos Pexels** | $0.00 | 200 req/hora gratuito |
| **YouTube Upload** | $0.00 | Gratuito |

**Total para uso 100% gratuito: $0.00**

## 🤖 Comparação de Modelos

| Modelo | Custo/Mês | Quota Gratuita | Custo/Token | Qualidade | Velocidade |
|--------|-----------|----------------|-------------|-----------|------------|
| **Grok** ⭐⭐⭐⭐⭐ | $0.00 🎉 | ∞ (sem limites) | $0.00 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Gemini** | $0.00 | Limitada (reseta/dia) | $0.00 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Claude 3.5** | $5 gratuito | 1000 req/dia | $3/1M | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **GPT-4** | Pago | Limitada | $0.03 input | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |  
| **GPT-3.5** | Pago | Limitada | $0.002 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**💡 Recomendação para uso 100% gratuito:** **Grok** - sem custos, sem limites!

## 🤝 Contribuição

Sinta-se à vontade para abrir issues e pull requests!

## 📄 Licença

Este projeto é open source. Use por sua conta e risco.