"""Command handlers for the bot."""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utils.constants import HELP_MESSAGE
from models.listing import Listing

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show marketplace statistics."""
    listings = context.bot_data.get('listings', [])
    total_listings = len(listings)
    category_stats = {}
    
    for listing in listings:
        category = listing['category']
        category_stats[category] = category_stats.get(category, 0) + 1
    
    stats_text = (
        "*📊 Marketplace Statistics*\n\n"
        f"*Total Listings:* {total_listings}\n\n"
        "*Listings by Category:*\n"
    )
    
    for category, count in category_stats.items():
        stats_text += f"• {category}: {count}\n"
    
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN) 