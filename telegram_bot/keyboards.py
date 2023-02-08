from telegram import ReplyKeyboardMarkup
import settings

SUPPORTED_ITEMS_KEYBOARD = [[*settings.SUPPORTED_TYPES]]
supported_items_reply_markup = ReplyKeyboardMarkup(
            SUPPORTED_ITEMS_KEYBOARD,
            one_time_keyboard=True,
            input_field_placeholder="Item type"
        )
