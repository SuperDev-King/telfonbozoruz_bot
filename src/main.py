"""Main application file for the Phone Marketplace Bot."""
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
from telegram.ext import ContextTypes

from utils.constants import (
    MAIN_MENU, POST_NAME, POST_CATEGORY, POST_DESCRIPTION, POST_PRICE, POST_PHOTO, SEARCH_NAME
)
from handlers.command_handlers import help_command, stats_command
from handlers.conversation_handlers import (
    start, handle_main_menu, handle_post_name, handle_category,
    handle_description, handle_price, handle_photo, handle_search_name
)

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Changed to DEBUG for more detailed logs
)

# Set up logging for telegram library
logging.getLogger('telegram').setLevel(logging.INFO)

def main() -> None:
    """Start the bot."""
    # Create the Application
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")
    
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))

    # Add conversation handler for posting
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(handle_main_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_name)
            ],
            POST_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_post_name)
            ],
            POST_CATEGORY: [
                CallbackQueryHandler(handle_category)
            ],
            POST_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description)
            ],
            POST_PRICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price)
            ],
            POST_PHOTO: [
                MessageHandler(filters.PHOTO, handle_photo)
            ]
        },
        fallbacks=[CommandHandler('start', start)],
        per_message=False,
        allow_reentry=True,
        name="phone_marketplace"
    )

    # Add the conversation handler first
    application.add_handler(conv_handler)

    # Add error handler with detailed logging
    def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and the update that caused it."""
        logging.error("Exception while handling an update:", exc_info=context.error)
        logging.error(f"Update {update} caused error {context.error}")

    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 