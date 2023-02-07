from telegram.ext import (
    Application, ConversationHandler,
    CommandHandler, MessageHandler, filters
    )

from handlers import Handler


class TelegramBot:
    def __init__(self, app: Application, handler: Handler) -> None:
        self.app = app
        self.handler = handler

        self.setup_handlers()

    def setup_handlers(self) -> None:
        self.app.add_handler(CommandHandler('start', self.handler.welcome))
        self.app.add_handler(CommandHandler('help', self.handler.help))

        add_discipline_handler = ConversationHandler(
            entry_points=[CommandHandler('add_discipline', self.handler.add_discipline)],
            states={
                0: [MessageHandler(filters.TEXT, self.handler.show_discipline_was_added)]
            },
            fallbacks=[CommandHandler('cancel', self.handler.cancel)]
        )
        self.app.add_handler(add_discipline_handler)
        self.app.add_handler(CommandHandler('list_disciplines', self.handler.list_disciplines))

    def run_polling(self) -> None:
        self.app.run_polling()
