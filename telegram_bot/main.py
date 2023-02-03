import logging

from telegram.ext import ApplicationBuilder, CommandHandler

import settings
import handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = ApplicationBuilder().token(settings.BOT_TOKEN).build()


def setup_handlers():
    app.add_handler(CommandHandler("start", handlers.welcome))
    app.add_handler(CommandHandler("help", handlers.help))


if __name__ == '__main__':
    setup_handlers()
    app.run_polling()
