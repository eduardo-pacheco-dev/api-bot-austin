import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Olá {user.first_name}! 👋\n\n"
        "Eu sou o api-bot-austin.\n"
        "Digite /help para ver os comandos disponíveis."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponíveis:\n\n"
        "/start - Iniciar o bot\n"
        "/hello - Dizer olá\n"
        "/help - Ver esta ajuda"
    )


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Olá {user.first_name}! Tudo bem por aí?")


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN não definido no arquivo .env")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("hello", hello))

    logger.info("Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling()


if __name__ == "__main__":
    main()
