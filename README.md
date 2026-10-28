# api-bot-austin

Projeto com FastAPI (endpoint `/health`) e Bot do Telegram (hello world).

## Pré-requisitos

- Python 3.10+
- Node.js e npm
- PM2 (global ou local)

Instalar PM2 globalmente:

```bash
npm install -g pm2
```

## Instalação

```bash
npm run setup  # Cria o venv e instala as dependências
npm install    # Instala dependências npm (apenas scripts)
cp .env.example .env
```

Edite o `.env` e adicione seu token do Telegram:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
```

## Executando com PM2 (modo desenvolvimento)

```bash
# Apenas API
npm run dev

# Apenas Bot do Telegram
npm run dev:bot

# API + Bot juntos
npm run dev:all
```

Outros comandos para gerenciar o estado:

```bash
npm run status   # Ver status dos processos
npm run logs     # Ver logs de todos
npm run logs:api # Logs apenas da API
npm run logs:bot # Logs apenas do bot
npm run restart  # Reiniciar
npm run stop     # Parar
npm run delete   # Remover do PM2
```

## Executando sem PM2

```bash
# API
uvicorn main:app --reload

# Bot
./venv/bin/python bot.py
```

**Endpoints:**
- API: `GET http://localhost:8000/health` → `{"status": "ok"}`
- Swagger: `http://localhost:8000/docs`

**Bot (comandos):**
- `/start` - Mensagem de boas-vindas
- `/hello` - Dizer olá
- `/help` - Lista de comandos

