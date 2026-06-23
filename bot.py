from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📥 تحميل فيديو", callback_data="video")],
        [InlineKeyboardButton("🎵 تحويل MP3", callback_data="mp3")],
    ]

    await update.message.reply_text(
        f"""
👋 أهلاً {update.effective_user.first_name}

🤖 بوت أبو كيان يرحب بك

━━━━━━━━━━━━━━

📥 تحميل الفيديوهات
🎵 تحويل الفيديو إلى MP3
⚡ سرعة وأداء ممتاز

━━━━━━━━━━━━━━

👑 المطور: أبو كيان
🛡️ جميع الحقوق محفوظة

اختر الخدمة من الأسفل 👇
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot Running...")
app.run_polling()
