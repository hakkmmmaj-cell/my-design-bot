from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📥 تحميل فيديو", callback_data="video")],
        [InlineKeyboardButton("🎵 تحويل MP3", callback_data="mp3")],
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")]
    ]

    await update.message.reply_text(
        f"""
👋 أهلاً وسهلاً {update.effective_user.first_name}

━━━━━━━━━━━━━━━━━━━━

🤖 بوت أبوك كيان في خدمتك

📥 تحميل فيديوهات TikTok
🎵 تحويل الفيديو إلى MP3
⚡ سرعة تحميل عالية

━━━━━━━━━━━━━━━━━━━━

👑 المطور: كيان
⚙️ جميع الحقوق محفوظة

اختر الخدمة من الأزرار بالأسفل 👇
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "video":
        await query.message.reply_text(
            "📥 أرسل رابط TikTok"
        )

    elif query.data == "mp3":
        await query.message.reply_text(
            "🎵 أرسل الرابط للتحويل MP3"
        )

    elif query.data == "stats":
        await query.message.reply_text(
            "📊 الإحصائيات غير مفعلة حالياً"
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Running...")

app.run_polling()
