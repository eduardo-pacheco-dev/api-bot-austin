# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- Endpoint `GET /bot/status` para monitoramento do bot do Telegram via PM2 com documentação completa no Swagger
- Bot do Telegram com `python-telegram-bot` (comandos `/start`, `/hello`, `/help`)
- Configuração PM2 para rodar bot separadamente (`ecosystem.bot.config.js`)
- Scripts npm para gerenciar API e bot juntos (`dev:bot`, `dev:all`, `logs:bot`)
- Arquivo `.env.example` para configuração do token do Telegram
- Configuração Nginx para proxy reverso (`nginx/api.austin.brazil.vps-kinghost.net`)
- Suporte a ambiente virtual `venv` com script `npm run setup`
- Skill `python-project-structure` adicionada ao projeto

### Changed
- API agora integrada com monitoramento do bot
- Atualização do `README.md` com instruções para API + Bot
- Configuração do PM2 ajustada para usar `venv`

### Fixed
- Correção na configuração do PM2 para executar via `venv/bin/uvicorn`

## [0.1.0] - 2026-10-28

### Added
- Projeto FastAPI inicial com endpoint `GET /health`
- Configuração PM2 com scripts npm para gerenciar estados
- Arquivo `requirements.txt` com dependências
- Documentação inicial no `README.md`
- `.gitignore` configurado
