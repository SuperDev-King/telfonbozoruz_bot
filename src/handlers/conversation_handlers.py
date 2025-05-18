"""Conversation handlers for the bot."""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utils.constants import (
    MAIN_MENU, POST_NAME, POST_CATEGORY, POST_DESCRIPTION, POST_PRICE, POST_PHOTO, SEARCH_NAME,
    PHONE_CATEGORIES, WELCOME_MESSAGE, HELP_MESSAGE
)
from models.listing import Listing

# Set up logging
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and show main menu."""
    # Initialize user's listings if not exists
    user_id = update.effective_user.id
    if 'user_listings' not in context.bot_data:
        context.bot_data['user_listings'] = {}
    if user_id not in context.bot_data['user_listings']:
        context.bot_data['user_listings'][user_id] = []

    keyboard = [
        [
            InlineKeyboardButton("📝 Telefon joylashtirish", callback_data='post'),
            InlineKeyboardButton("🔍 Telefonlarni qidirish", callback_data='search')
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data='stats'),
            InlineKeyboardButton("📱 Mening e'lonlarim", callback_data='my_posts')
        ],
        [
            InlineKeyboardButton("❓ Yordam", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.callback_query.edit_message_text(WELCOME_MESSAGE, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    return MAIN_MENU

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle main menu button presses."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    logger.info(f"Main menu handler called with data: {query.data}")
    logger.info(f"Current user_data: {context.user_data}")

    if query.data == 'post':
        await query.edit_message_text(
            "*Telefonni sotishga joylashtirishni boshlaymiz!* 📱\n\n"
            "Iltimos, telefon nomini kiriting:",
            parse_mode=ParseMode.MARKDOWN
        )
        return POST_NAME
    elif query.data == 'search':
        # Create keyboard with two columns
        categories = list(PHONE_CATEGORIES.items())
        keyboard = []
        for i in range(0, len(categories), 2):
            row = []
            row.append(InlineKeyboardButton(categories[i][1], callback_data=f'search_{categories[i][0]}'))
            if i + 1 < len(categories):
                row.append(InlineKeyboardButton(categories[i + 1][1], callback_data=f'search_{categories[i + 1][0]}'))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "*Qidirish uchun kategoriyani tanlang:*",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return MAIN_MENU
    elif query.data == 'my_posts':
        user_listings = context.bot_data['user_listings'].get(user_id, [])
        
        if not user_listings:
            keyboard = [[InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "*Siz hali hech qanday telefon joylashtirmagansiz.*\n\n"
                "Menyuga qaytish uchun quyidagi tugmani bosing.",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            return MAIN_MENU
        
        # Send each listing with delete button
        for i, listing in enumerate(user_listings):
            caption = (
                f"*{listing['name']}*\n\n"
                f"💰 *Narx:* {listing['price']}\n"
                f"📝 *Tavsif:* {listing['description']}\n"
                f"*Kategoriya:* {PHONE_CATEGORIES[listing['category']]}"
            )
            keyboard = [[InlineKeyboardButton("🗑️ E'lonni o'chirish", callback_data=f'delete_{i}')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_photo(
                photo=listing['photo_id'],
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        keyboard = [[InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "*Menyuga qaytish uchun quyidagi tugmani bosing.*",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return MAIN_MENU
    elif query.data.startswith('delete_'):
        index = int(query.data.split('_')[1])
        user_listings = context.bot_data['user_listings'].get(user_id, [])
        
        if 0 <= index < len(user_listings):
            user_listings.pop(index)
            # Send a new message instead of editing
            await query.message.reply_text(
                "*✅ E'loningiz muvaffaqiyatli o'chirildi!*\n\n"
                "Menyuga qaytish uchun quyidagi tugmani bosing.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]]),
                parse_mode=ParseMode.MARKDOWN
            )
            # Delete the original message with the photo
            try:
                await query.message.delete()
            except Exception:
                pass  # Ignore if we can't delete the message
        
        return MAIN_MENU
    elif query.data == 'stats':
        # Get all listings from all users
        all_listings = []
        for user_listings in context.bot_data['user_listings'].values():
            all_listings.extend(user_listings)
            
        total_listings = len(all_listings)
        category_stats = {}
        for listing in all_listings:
            category = listing['category']
            category_stats[category] = category_stats.get(category, 0) + 1
        
        stats_text = (
            "*📊 Bozor statistikasi*\n\n"
            f"*Jami e'lonlar:* {total_listings}\n\n"
            "*Kategoriyalar bo'yicha:*\n"
        )
        
        for category, count in category_stats.items():
            stats_text += f"• {PHONE_CATEGORIES[category]}: {count}\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return MAIN_MENU
    elif query.data == 'help':
        keyboard = [[InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(HELP_MESSAGE, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return MAIN_MENU
    elif query.data == 'back_to_menu':
        logger.info("Back to menu button pressed")
        return await start(update, context)
    elif query.data == 'search_by_name':
        logger.info("Search by name button pressed")
        category = context.user_data.get('search_category')
        logger.info(f"Current search category: {category}")
        
        if not category:
            logger.warning("No search category found in user_data")
            return await start(update, context)
            
        # Delete the previous message with buttons
        try:
            await query.message.delete()
            logger.info("Previous message deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete previous message: {e}")
            
        # Send a new message asking for the phone name
        logger.info("Sending search prompt message")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Iltimos, qidirish uchun telefon nomini kiriting:*\n\n"
                 "Misol: iPhone 13, Samsung S21, Xiaomi 12",
            parse_mode=ParseMode.MARKDOWN
        )
        # Set flag to indicate we're waiting for search input
        context.user_data['waiting_for_search'] = True
        logger.info(f"Set waiting_for_search flag. Current user_data: {context.user_data}")
        return MAIN_MENU
    elif query.data.startswith('search_'):
        # Extract category from callback data
        category = query.data.replace('search_', '')
        logger.info(f"Search category selected: {category}")
        
        if category not in PHONE_CATEGORIES:
            logger.warning(f"Invalid category selected: {category}")
            return await start(update, context)
            
        context.user_data['search_category'] = category
        logger.info(f"Search category stored in user_data: {context.user_data}")
        
        keyboard = [
            [
                InlineKeyboardButton("🔍 Nomi bo'yicha qidirish", callback_data='search_by_name'),
                InlineKeyboardButton("📱 Barcha telefonlarni ko'rish", callback_data='show_all')
            ],
            [InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"*{PHONE_CATEGORIES[category]} kategoriyasida qanday qidirishni xohlaysiz?*",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return MAIN_MENU
    elif query.data == 'show_all':
        category = context.user_data.get('search_category')
        if not category:
            return await start(update, context)
            
        # Get all listings from all users
        all_listings = []
        for user_listings in context.bot_data['user_listings'].values():
            all_listings.extend(user_listings)
            
        found_listings = [listing for listing in all_listings if listing['category'] == category]
        
        if not found_listings:
            keyboard = [[InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"❌ {PHONE_CATEGORIES[category]} kategoriyasida telefonlar topilmadi.\n\n"
                "Menyuga qaytish uchun quyidagi tugmani bosing.",
                reply_markup=reply_markup
            )
            return MAIN_MENU
        
        # Send all listings
        await query.message.reply_text(
            f"✅ {PHONE_CATEGORIES[category]} kategoriyasida {len(found_listings)} ta telefon topildi:\n\n"
            "Quyidagi natijalarni ko'rib chiqing:"
        )
        
        for listing in found_listings:
            caption = (
                f"{listing['name']}\n\n"
                f"💰 Narx: {listing['price']}\n"
                f"📝 Tavsif: {listing['description']}\n"
                f"👤 Sotuvchi: @{listing['username']}\n\n"
                f"Kategoriya: {PHONE_CATEGORIES[listing['category']]}"
            )
            try:
                await query.message.reply_photo(
                    photo=listing['photo_id'],
                    caption=caption
                )
            except Exception as e:
                await query.message.reply_text(caption)
        
        keyboard = [[InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "Qidiruv yakunlandi.\n\n"
            "Menyuga qaytish uchun quyidagi tugmani bosing.",
            reply_markup=reply_markup
        )
        return MAIN_MENU

async def handle_search_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone name search input."""
    logger.info("Search name handler called")
    logger.info(f"Current user_data: {context.user_data}")
    
    # Check if we're waiting for search input
    if not context.user_data.get('waiting_for_search'):
        logger.warning("Not waiting for search input, returning to main menu")
        return MAIN_MENU
        
    search_query = update.message.text.lower()
    logger.info(f"Search query received: {search_query}")
    
    category = context.user_data.get('search_category')
    logger.info(f"Search category: {category}")
    
    if not category:
        logger.warning("No search category found in user_data")
        return await start(update, context)
    
    # Get all listings from all users
    all_listings = []
    if 'user_listings' not in context.bot_data:
        logger.warning("No user_listings in bot_data")
        context.bot_data['user_listings'] = {}
    
    for user_listings in context.bot_data['user_listings'].values():
        all_listings.extend(user_listings)
    
    logger.info(f"Total listings found: {len(all_listings)}")
    
    # Filter by category and search query
    found_listings = [
        listing for listing in all_listings 
        if listing['category'] == category and search_query in listing['name'].lower()
    ]
    
    logger.info(f"Found {len(found_listings)} listings matching search query")
    
    if not found_listings:
        keyboard = [
            [
                InlineKeyboardButton("🔄 Qayta qidirish", callback_data=f'search_{category}'),
                InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"❌ '{search_query}' so'zi bo'yicha {PHONE_CATEGORIES[category]} kategoriyasida telefonlar topilmadi.\n\n"
            "Quyidagi variantlardan birini tanlang:\n"
            "• Qayta qidirish - boshqa nom bilan qidirish\n"
            "• Menyuga qaytish - asosiy menyuga qaytish",
            reply_markup=reply_markup
        )
        context.user_data.pop('waiting_for_search', None)
        return MAIN_MENU
    
    # Send found listings
    await update.message.reply_text(
        f"✅ '{search_query}' so'zi bo'yicha {len(found_listings)} ta telefon topildi:\n\n"
        "Quyidagi natijalarni ko'rib chiqing:"
    )
    
    for listing in found_listings:
        caption = (
            f"{listing['name']}\n\n"
            f"💰 Narx: {listing['price']}\n"
            f"📝 Tavsif: {listing['description']}\n"
            f"👤 Sotuvchi: @{listing['username']}\n\n"
            f"Kategoriya: {PHONE_CATEGORIES[listing['category']]}"
        )
        
        try:
            # Send photo with caption
            await update.message.reply_photo(
                photo=listing['photo_id'],
                caption=caption
            )
        except Exception as e:
            logger.error(f"Failed to send photo: {e}")
            # If photo sending fails, send as text
            await update.message.reply_text(caption)
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Qayta qidirish", callback_data=f'search_{category}'),
            InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Qidiruv yakunlandi.\n\n"
        "Quyidagi variantlardan birini tanlang:\n"
        "• Qayta qidirish - boshqa nom bilan qidirish\n"
        "• Menyuga qaytish - asosiy menyuga qaytish",
        reply_markup=reply_markup
    )
    context.user_data.pop('waiting_for_search', None)
    return MAIN_MENU

async def handle_post_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle phone name input."""
    context.user_data['phone_name'] = update.message.text
    # Create keyboard with two columns
    categories = list(PHONE_CATEGORIES.items())
    keyboard = []
    for i in range(0, len(categories), 2):
        row = []
        row.append(InlineKeyboardButton(categories[i][1], callback_data=f'category_{categories[i][0]}'))
        if i + 1 < len(categories):
            row.append(InlineKeyboardButton(categories[i + 1][1], callback_data=f'category_{categories[i + 1][0]}'))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "*Telefon kategoriyasini tanlang:*",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return POST_CATEGORY

async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle category selection."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('category_'):
        context.user_data['category'] = query.data.split('_')[1]
        await query.edit_message_text(
            "*Iltimos, telefon haqida tavsif kiriting:*\n\n"
            "Quyidagi ma'lumotlarni kiriting:\n"
            "• Holati\n"
            "• Xotira hajmi\n"
            "• Rangi\n"
            "• Qo'shimcha aksessuarlar",
            parse_mode=ParseMode.MARKDOWN
        )
        return POST_DESCRIPTION
    return POST_CATEGORY

async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle description input."""
    context.user_data['description'] = update.message.text
    await update.message.reply_text(
        "*Iltimos, narxni kiriting:*\n\n"
        "Format: [summa] [valyuta]\n"
        "Misol: 500 USD",
        parse_mode=ParseMode.MARKDOWN
    )
    return POST_PRICE

async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle price input."""
    context.user_data['price'] = update.message.text
    await update.message.reply_text(
        "*Iltimos, telefon rasmini yuboring:*\n\n"
        "Rasm aniq va telefonning holatini ko'rsatishi kerak.",
        parse_mode=ParseMode.MARKDOWN
    )
    return POST_PHOTO

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle photo upload."""
    photo = update.message.photo[-1]
    context.user_data['photo_id'] = photo.file_id
    
    # Get username or first name
    username = update.effective_user.username
    if not username:
        username = update.effective_user.first_name
    
    # Create the listing
    listing = Listing(
        name=context.user_data['phone_name'],
        category=context.user_data['category'],
        description=context.user_data['description'],
        price=context.user_data['price'],
        photo_id=context.user_data['photo_id'],
        username=username
    )
    
    # Store in user's listings
    user_id = update.effective_user.id
    if 'user_listings' not in context.bot_data:
        context.bot_data['user_listings'] = {}
    if user_id not in context.bot_data['user_listings']:
        context.bot_data['user_listings'][user_id] = []
    
    context.bot_data['user_listings'][user_id].append(listing.to_dict())
    
    # Clear user data
    context.user_data.clear()
    
    keyboard = [[InlineKeyboardButton("🔙 Menyuga qaytish", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "*✅ Telefoningiz muvaffaqiyatli joylashtirildi!*\n\n"
        "Menyuga qaytish uchun quyidagi tugmani bosing.",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return MAIN_MENU 