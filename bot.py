import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

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
            "outtmpl": "%(title)s.%(ext)s",
            "noplaylist": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        size = os.path.getsize(filename)

        if size < 50 * 1024 * 1024:
            with open(filename, "rb") as video:
                await update.message.reply_video(video)
        else:
            await update.message.reply_document(open(filename, "rb"))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ:\n{e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("✅ Bot Started")
app.run_polling()
