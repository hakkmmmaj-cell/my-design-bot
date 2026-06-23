from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
Application,
CommandHandler,
CallbackQueryHandler,
ContextTypes
)

BOT_TOKEN = "PUT_NEW_TOKEN_HERE"

CHANNEL_USERNAME = "@A_1_1_1W"

async def check_subscription(user_id, bot):
try:
member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
return member.status in ["member", "administrator", "creator"]
except:
return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

user_id = update.effective_user.id

if not await check_subscription(user_id, context.bot):
    await update.message.reply_text(
        "🚫 يجب الاشتراك بقناة أبو كيان أولاً:\nhttps://t.me/A_1_1_1W\n\nثم أرسل /start"
    )
    return

keyboard = [
    [InlineKeyboardButton("📥 تحميل فيديو", callback_data="video")],
    [InlineKeyboardButton("🎵 تحويل MP3", callback_data="mp3")]
]

await update.message.reply_text(
    f"""

👋 أهلاً {update.effective_user.first_name}

🤖 بوت أبو كيان يرحب بك

━━━━━━━━━━━━━━

📥 تحميل الفيديوهات
🎵 تحويل الفيديو إلى MP3

━━━━━━━━━━━━━━

👑 المطور: أبو كيان
🛡️ جميع الحقوق محفوظة

اختر الخدمة من الأسفل 👇
""",
reply_markup=InlineKeyboardMarkup(keyboard)
)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

if query.data == "video":
    await query.message.reply_text("📥 أرسل رابط TikTok")

elif query.data == "mp3":
    await query.message.reply_text("🎵 أرسل رابط الفيديو للتحويل إلى MP3")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Running...")
app.run_polling()
