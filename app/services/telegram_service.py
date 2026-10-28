import html
import json
import logging
import urllib.error
import urllib.request
from datetime import datetime

from app.core.config import settings
from app.models.ndpd_log import NdpdLog

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def _format_value(value: object | None, default: str = "Não informado") -> str:
    if value is None or value == "":
        return default
    return html.escape(str(value))


def _format_quantity(value: float | None) -> str:
    if value is None:
        return "0"
    number = float(value)
    return str(int(number)) if number.is_integer() else f"{number:g}"


def _format_datetime(value: datetime | None) -> str:
    if value is None:
        return "Não informado"
    return value.strftime("%d/%m/%Y %H:%M:%S")


def build_ndpd_log_message(log: NdpdLog) -> str:
    """Monta a mensagem de log de vistoria enviada ao Telegram."""
    data_hora = log.event_datetime or log.created_at
    return "\n".join(
        [
            "📋 LOG DE VISTORIA / RELATÓRIO",
            "────────────────────────────",
            f"🏢 Site-ID: {_format_value(log.site_id)}",
            f"📑 Relatório: {_format_value(log.report)}",
            f"📄 OC: {_format_value(log.oc)}",
            f"🛠 OS: {_format_value(log.so)}",
            "",
            f"📦 Item: {_format_value(log.item_name)}",
            f"📌 Status: {_format_value(log.status)}",
            "",
            "📊 RESUMO DE QUANTIDADES",
            f"- 🟢 Aprovadas: {_format_quantity(log.quantity_approved)}",
            f"- 🟡 Pendentes: {_format_quantity(log.quantity_pending)}",
            f"- 🔴 Reprovadas: {_format_quantity(log.quantity_rejected)}",
            f"- 📈 Total: {_format_quantity(log.quantity_total)}",
            "",
            "⚠️ Motivo da Reprovação:",
            _format_value(log.rejection_reason),
            "────────────────────────────",
            f"⏰ <b>Enviado em: {_format_datetime(data_hora)}</b>",
        ]
    )


def send_telegram_message(text: str) -> bool:
    """Envia uma mensagem para o chat configurado em TELEGRAM_CHAT_ID."""
    token = settings.telegram_bot_token
    chat_id = settings.telegram_chat_id

    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN não configurado; notificação não enviada.")
        return False

    if not chat_id:
        logger.warning("TELEGRAM_CHAT_ID não configurado; notificação não enviada.")
        return False

    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        TELEGRAM_API_URL.format(token=token),
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 200:
                logger.error(
                    "Falha ao enviar notificação ao Telegram (HTTP %s): %s",
                    response.status,
                    response.read().decode("utf-8", errors="replace"),
                )
                return False
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        logger.error("Falha ao enviar notificação ao Telegram: %s", detail)
        return False
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        logger.error("Erro de conexão ao enviar notificação ao Telegram: %s", exc)
        return False

    logger.info("Notificação de log NDPD enviada ao Telegram.")
    return True
