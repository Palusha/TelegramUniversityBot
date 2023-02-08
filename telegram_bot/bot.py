from telegram.ext import (
    Application, CallbackQueryHandler, ConversationHandler,
    CommandHandler, MessageHandler, filters
    )

import handlers
from handlers import Handler


class TelegramBot:
    def __init__(self, app: Application, handler: Handler) -> None:
        self.app = app
        self.handler = handler

        self.setup_handlers()

    def setup_handlers(self) -> None:
        cancel_handler = CommandHandler('cancel', self.handler.cancel)

        self.app.add_handler(CommandHandler('start', self.handler.welcome))
        self.app.add_handler(CommandHandler('help', self.handler.help))

        add_discipline_handler = ConversationHandler(
            entry_points=[CommandHandler('add_discipline', self.handler.add_discipline)],
            states={
                0: [MessageHandler(filters.TEXT, self.handler.show_discipline_was_added)]
            },
            fallbacks=[cancel_handler]
        )
        self.app.add_handler(add_discipline_handler)

        list_discipline_handler = ConversationHandler(
            entry_points=[CommandHandler('list_disciplines', self.handler.list_disciplines)],
            states={
                0: [CallbackQueryHandler(self.handler.handle_discipline_items_list, pattern='^list-disciplines:.+$')]
            },
            fallbacks=[cancel_handler]
        )
        self.app.add_handler(list_discipline_handler)

        add_discipline_item_handler = ConversationHandler(
            entry_points=[CommandHandler('add_discipline_item', self.handler.add_discipline_item)],
            states={
                0: [CallbackQueryHandler(self.handler.handle_add_discipline_item, pattern='^add-item:.+$')],
                1: [MessageHandler(filters.TEXT, self.handler.handle_entered_item_type)],
                2: [MessageHandler(filters.TEXT, self.handler.show_discipline_item_was_added)]
            },
            fallbacks=[cancel_handler]
        )
        self.app.add_handler(add_discipline_item_handler)

        delete_discipline_handler = ConversationHandler(
            entry_points=[CommandHandler('remove_discipline', self.handler.remove_discipline)],
            states={
                0: [CallbackQueryHandler(self.handler.handle_remove_discipline, pattern='^remove-discipline:.+$')]
            },
            fallbacks=[cancel_handler]
        )
        self.app.add_handler(delete_discipline_handler)

        self.app.add_error_handler(self.handler.error_handler)

    def run_polling(self) -> None:
        self.app.run_polling()
