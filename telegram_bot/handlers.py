
from telegram.ext import ContextTypes
from telegram import Update


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Welcome, {update.effective_user.first_name}. I\'m study bot.\nType /help to see all commands.')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Commands will be added in future updates. Thank you for your patience.')
