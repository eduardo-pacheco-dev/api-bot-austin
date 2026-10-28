# api-bot-austin

Projeto FastAPI mínimo com apenas o endpoint de saúde.

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
```

## Executando com PM2 (modo desenvolvimento)

```bash
npm run dev
```

Outros comandos para gerenciar o estado:

```bash
npm run status   # Ver status dos processos
npm run logs     # Ver logs em tempo real
npm run restart  # Reiniciar aplicação
npm run reload   # Reload sem downtime
npm run stop     # Parar aplicação
npm run delete   # Remover do PM2
```

## Executando sem PM2

```bash
uvicorn main:app --reload
```

Endpoint: `GET http://localhost:8000/health` retorna `{"status": "ok"}`.
