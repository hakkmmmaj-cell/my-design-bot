from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 بوت أبو كيان يرحب بك\n\n"
        "📥 أرسل رابط يوتيوب أو تيك توك للتحميل."
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    await update.message.reply_text("⏳ جاري التحميل...")

    try:
        ydl_opts = {
            "format": "best",
            "outtmpl": "video.%(ext)s",
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        file_name = None
        for f in os.listdir():
            if f.startswith("video."):
                file_name = f
                break

        if file_name:
            with open(file_name, "rb") as video:
                await update.message.reply_video(video)

            os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("✅ Bot Started")
app.run_polling()
