from fastapi import FastAPI
from pydantic import BaseModel, Field
import psutil
import subprocess
import json
from typing import Literal

app = FastAPI(
    title="api-bot-austin",
    description="API com endpoint health e monitoramento do bot do Telegram",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


class HealthResponse(BaseModel):
    status: Literal["ok"] = Field(
        ..., description="Status da API", example="ok"
    )


class BotStatusRunningResponse(BaseModel):
    status: Literal["running"] = Field(
        ..., description="Status do bot", example="running"
    )
    pid: int = Field(..., description="Process ID do bot no sistema", example=35817)
    name: str = Field(
        ..., description="Nome do processo no PM2", example="api-bot-austin-telegram"
    )
    uptime: int | None = Field(
        None, description="Timestamp de início (Unix ms) conforme PM2", example=1793205728669
    )
    restarts: int = Field(
        ..., description="Número de reinicializações", example=62
    )


class BotStatusOtherResponse(BaseModel):
    status: str = Field(
        ..., description="Status do bot conforme PM2", example="stopped"
    )
    name: str = Field(
        ..., description="Nome do processo no PM2", example="api-bot-austin-telegram"
    )


class BotStatusStoppedResponse(BaseModel):
    status: Literal["stopped"] = Field(
        ..., description="Status do bot", example="stopped"
    )
    name: str = Field(
        ..., description="Nome do processo no PM2", example="api-bot-austin-telegram"
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Verifica saúde da API",
    description="Endpoint simples para verificar se a API está no ar.",
    responses={
        200: {
            "description": "API está funcionando normalmente",
            "model": HealthResponse,
        }
    },
)
def health():
    return {"status": "ok"}


@app.get(
    "/bot/status",
    response_model=BotStatusRunningResponse | BotStatusOtherResponse | BotStatusStoppedResponse,
    tags=["Bot"],
    summary="Verifica status do bot do Telegram",
    description=(
        "Retorna o status atual do bot do Telegram gerenciado pelo PM2. "
        "Consulta via `pm2 jlist` e faz fallback por busca de processos caso necessário."
    ),
    responses={
        200: {
            "description": "Status do bot retornado com sucesso",
            "content": {
                "application/json": {
                    "examples": {
                        "running": {
                            "summary": "Bot em execução",
                            "value": {
                                "status": "running",
                                "pid": 35817,
                                "name": "api-bot-austin-telegram",
                                "uptime": 1793205728669,
                                "restarts": 62,
                            },
                        },
                        "stopped": {
                            "summary": "Bot parado",
                            "value": {"status": "stopped", "name": "api-bot-austin-telegram"},
                        },
                        "errored": {
                            "summary": "Bot com erro",
                            "value": {"status": "errored", "name": "api-bot-austin-telegram"},
                        },
                    }
                }
            },
        }
    },
)
def bot_status():
    """Verifica o status do bot do Telegram rodando via PM2"""
    try:
        result = subprocess.run(
            ["pm2", "jlist"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout:
            processes = json.loads(result.stdout)
            for proc in processes:
                if proc.get("name") == "api-bot-austin-telegram":
                    pm2_env = proc.get("pm2_env", {})
                    status = pm2_env.get("status")
                    if status == "online":
                        return {
                            "status": "running",
                            "pid": proc.get("pid"),
                            "name": proc.get("name"),
                            "uptime": pm2_env.get("pm_uptime"),
                            "restarts": pm2_env.get("restart_time", 0),
                        }
                    return {"status": status, "name": proc.get("name")}
    except Exception:
        pass

    # Fallback: verifica diretamente pelos processos
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmdline = proc.info.get("cmdline") or []
            cmdline_str = " ".join(cmdline)
            if "bot.py" in cmdline_str and "/root/workstation/api-bot-austin" in cmdline_str:
                return {
                    "status": "running",
                    "pid": proc.info["pid"],
                    "name": "api-bot-austin-telegram",
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return {"status": "stopped", "name": "api-bot-austin-telegram"}
