import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

keyboard = [
    ["🔎 Sotuvchini tekshirish"],
    ["🛡 Xavfsiz xarid", "📁 Dalillarni saqlash"],
    ["⚖️ Huquqiy yordam"],
    ["📝 Shikoyat tayyorlash"],
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! LEXGUARD botiga xush kelibsiz!\n\n"
        "LEXGUARD — xavfsiz onlayn xarid va huquqiy yordam platformasi.\n"
        "Kerakli xizmatni tanlang:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True
        ),
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    responses = {
        "🔎 Sotuvchini tekshirish":
            "Sotuvchi haqidagi ma'lumotlarni yuborish bo‘limi. "
            "Bu funksiya hozir ishlab chiqilmoqda.",
        "🛡 Xavfsiz xarid":
            "Onlayn xarid qilishda shartnoma, to‘lov va sotuvchi "
            "ma'lumotlarini tekshiring.",
        "📁 Dalillarni saqlash":
            "Xaridga oid chek, yozishma va boshqa hujjatlarni "
            "saqlab qo‘ying. Bu funksiya ishlab chiqilmoqda.",
        "⚖️ Huquqiy yordam":
            "Muammoingizni qisqacha yozing. Sizga umumiy huquqiy "
            "ma'lumot berishga yordam beramiz.",
        "📝 Shikoyat tayyorlash":
            "Shikoyat tayyorlash bo‘limi hozir ishlab chiqilmoqda.",
    }

    answer = responses.get(
        text,
        "Iltimos, menyudagi xizmatlardan birini tanlang."
    )
    await update.message.reply_text(answer)

def main():
    if not TOKEN or not WEBHOOK_URL or not WEBHOOK_SECRET:
        raise RuntimeError("Kerakli muhit o‘zgaruvchilari kiritilmagan!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))

    print("LEXGUARD ishga tushmoqda...")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path="telegram",
        webhook_url=f"{WEBHOOK_URL.rstrip('/')}/telegram",
        secret_token=WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES,
    )

if __name__ == "__main__":
    main()
