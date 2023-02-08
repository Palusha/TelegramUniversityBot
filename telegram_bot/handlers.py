import html
import json
import traceback
from datetime import datetime

from telegram import ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from database.db import DataBase
from keyboards import supported_items_reply_markup
from utils import get_callback_query_data

DEVELOPER_CHAT_ID = 365771922
SHOW_DISCIPLINE_WAS_ADDED = HANDLE_DISCIPLINES_ITEMS_LIST = HANDLE_ADD_DISCIPLINE_ITEM = HANDLE_REMOVE_DISCIPLINE = 0
HANDLE_ENTER_ITEM_TYPE = 1
SHOW_DISCIPLINE_ITEM_WAS_ADDED = 2


class Handler:
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

        return SHOW_DISCIPLINE_WAS_ADDED

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
        keyboard = []

        for discipline in disciplines_list:
            keyboard.append([InlineKeyboardButton(
                discipline['discipline_name'],
                callback_data=f'list-disciplines:{discipline["discipline_name"]}'
                 )])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Disciplines:', reply_markup=reply_markup)

        return HANDLE_DISCIPLINES_ITEMS_LIST

    async def handle_discipline_items_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        discipline_name = get_callback_query_data(query.data)
        discipline_items = self.database.get_discipline_items(update.effective_user.id, discipline_name)

        await query.answer()

        if discipline_items:
            message = ''
            for item in discipline_items:
                formatted_date = item["date_added"].strftime('%d.%m.%Y')
                message += f'Date added - {formatted_date}\n\n'
                message += item['item_content']

            await query.edit_message_text(f'Here are items for {discipline_name}')
            await query.message.reply_text(message)
        else:
            await query.edit_message_text(f'{discipline_name} has no items')

        return ConversationHandler.END

    async def add_discipline_item(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = []
        disciplines_list = self.database.list_disciplines(update.effective_user.id)

        for discipline in disciplines_list:
            keyboard.append([InlineKeyboardButton(
                discipline['discipline_name'],
                callback_data=f'add-item:{discipline["discipline_name"]}'
                )])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Choose discipline:', reply_markup=reply_markup)

        return HANDLE_ADD_DISCIPLINE_ITEM

    async def handle_add_discipline_item(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        context.user_data['discipline_name'] = get_callback_query_data(query.data)

        await query.answer()
        await query.delete_message()
        await query.message.reply_text('Enter supported item type', reply_markup=supported_items_reply_markup)

        return HANDLE_ENTER_ITEM_TYPE

    async def handle_entered_item_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message_text = update.message.text
        if message_text == 'text':
            context.user_data['item_type'] = message_text

            await update.message.reply_text('Enter text')
        else:
            await update.message.reply_text(
                f'Entered type "{message_text}" is not supported.\nEnter supported item type',
                reply_markup=supported_items_reply_markup
                )

            return HANDLE_ENTER_ITEM_TYPE

        return SHOW_DISCIPLINE_ITEM_WAS_ADDED

    async def show_discipline_item_was_added(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        discipline_name = context.user_data.pop('discipline_name')

        item_data = {
            'item_type': context.user_data.pop('item_type'),
            'item_content': update.message.text,
            'date_added': datetime.now()
        }

        self.database.add_item_to_discipline(user_id, discipline_name, item_data)

        await update.message.reply_text('Item was added')

        return ConversationHandler.END

    async def remove_discipline(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        disciplines_list = self.database.list_disciplines(update.effective_user.id)
        keyboard = []

        for discipline in disciplines_list:
            keyboard.append([InlineKeyboardButton(
                discipline['discipline_name'],
                callback_data=f'remove-discipline:{discipline["_id"]}'
                )])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text('Choose discipline to delete', reply_markup=reply_markup)

        return HANDLE_REMOVE_DISCIPLINE

    async def handle_remove_discipline(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        document_id = get_callback_query_data(query.data)

        self.database.remove_discipline(document_id)

        await query.answer()
        await query.edit_message_text('Discipline was deleted')

        return ConversationHandler.END

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)

        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096 character limit.
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            f"An exception was raised while handling an update\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
            f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        await context.bot.send_message(
            chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
        )
