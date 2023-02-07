from telegram.ext import ApplicationBuilder

import settings
from bot import TelegramBot
from database.db import DataBase
from handlers import Handler


if __name__ == '__main__':
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    db = DataBase(db_uri=settings.DB_URI, db_name=settings.DB_NAME)
    handler = Handler(database=db)
    bot = TelegramBot(app=app, handler=handler)
    bot.run_polling()
