"""Constants for the Phone Marketplace Bot."""
from telegram.ext import ConversationHandler

# Conversation states
MAIN_MENU, POST_NAME, POST_CATEGORY, POST_DESCRIPTION, POST_PRICE, POST_PHOTO, SEARCH_NAME = range(7)

# Phone categories with emojis
PHONE_CATEGORIES = {
    'iphone': '📱 iPhone',
    'samsung': '📱 Samsung',
    'xiaomi': '📱 Xiaomi',
    'huawei': '📱 Huawei',
    'vivo': '📱 Vivo',
    'oppo': '📱 OPPO',
    'realme': '📱 Realme',
    'honor': '📱 Honor',
    'nokia': '📱 Nokia',
    'tecno': '📱 Tecno',
    'infinix': '📱 Infinix',
    'other': '📱 Boshqa'
}

# Welcome message
WELCOME_MESSAGE = (
    "Telefon Bozor Botiga xush kelibsiz! 🏪\n\n"
    "Bu yerda siz:\n"
    "• Telefonlarni sotishga joylashtirishingiz mumkin\n"
    "• Telefonlarni qidirishingiz mumkin\n"
    "• Bozor statistikasini ko'rishingiz mumkin\n"
    "• Yordam olishingiz mumkin\n\n"
    "Boshlash uchun quyidagi tugmalardan foydalaning!"
)

# Help message
HELP_MESSAGE = (
    "📱 *Telefon Bozor Boti Yordami*\n\n"
    "*Mavjud buyruqlar:*\n"
    "• /start - Botni ishga tushirish\n"
    "• /help - Yordam xabarini ko'rsatish\n"
    "• /stats - Bozor statistikasini ko'rsatish\n\n"
    "*Telefon joylashtirish uchun:*\n"
    "1. 'Telefon joylashtirish' tugmasini bosing\n"
    "2. Telefon nomini kiriting\n"
    "3. Kategoriyani tanlang\n"
    "4. Tavsif qo'shing\n"
    "5. Narxni belgilang\n"
    "6. Rasm yuboring\n\n"
    "*Qidirish uchun:*\n"
    "1. 'Telefonlarni qidirish' tugmasini bosing\n"
    "2. Kategoriyani tanlang\n"
    "3. Telefon nomini kiriting yoki barcha telefonlarni ko'ring\n\n"
    "*Imkoniyatlar:*\n"
    "• Bir nechta telefon joylashtirish\n"
    "• Kategoriya bo'yicha qidirish\n"
    "• Bozor statistikasini ko'rish\n"
    "• O'z e'lonlaringizni o'chirish\n\n"
    "Qo'shimcha yordam kerakmi? Bot administratoriga murojaat qiling."
) 