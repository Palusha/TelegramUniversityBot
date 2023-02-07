from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from database.db import DataBase


class Handler:
    SHOW_DISCIPLINE_WAS_ADDED = 0

    def __init__(self, database: DataBase) -> None:
        self.database = database

    async def welcome(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            f'Welcome, {update.effective_user.first_name}. I\'m study bot.\nType /help to see all commands.'
            )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Commands will be added in future updates. Thank you for your patience.')

    async def add_discipline(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Enter discipline name.')

        return self.SHOW_DISCIPLINE_WAS_ADDED

    async def show_discipline_was_added(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        discipline_name = update.message.text
        self.database.add_discipline(discipline_name, update.effective_user.id)

        await update.message.reply_text(f'Discipline: {discipline_name} was added to your list.')

        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        '''Cancels and ends the operation.'''
        await update.message.reply_text(
            'Cancelled', reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    async def list_disciplines(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        disciplines_list = self.database.list_disciplines(update.effective_user.id)

        message = 'Disciplines:\n'
        for discipline in disciplines_list:
            message += f'- {discipline["discipline_name"]}\n'

        await update.message.reply_text(message)
