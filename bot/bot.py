import os
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from config import BOT_TOKEN
from db import init_db, add_user, add_download, get_stats
from downloader import download_video
from mp3 import convert_to_mp3

init_db()


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    add_user(user.id, user.username, str(datetime.now()))

    keyboard = [
        [InlineKeyboardButton("📥 تحميل فيديو", callback_data="dl")],
        [InlineKeyboardButton("🎵 تحويل MP3", callback_data="mp3")],
        [InlineKeyboardButton("📊 إحصائيات", callback_data="stats")]
    ]

    await update.message.reply_text(
        "🔥 أهلاً بك في بوت التحميل الاحترافي",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# BUTTONS
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "stats":
        users, downloads = get_stats()
        await q.edit_message_text(f"👥 المستخدمين: {users}\n📥 التحميلات: {downloads}")

    elif q.data == "dl":
        await q.edit_message_text("📥 أرسل رابط الفيديو")

    elif q.data == "mp3":
        await q.edit_message_text("🎵 أرسل رابط لتحويله MP3")


# HANDLE LINKS
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("⏳ جاري المعالجة...")

    try:
        file_path, info = download_video(url)

        add_download(update.message.from_user.id, url, "video", str(datetime.now()))

        await update.message.reply_video(video=open(file_path, "rb"))

        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ خطأ: {e}")


# MAIN
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot Running...")
app.run_polling()
