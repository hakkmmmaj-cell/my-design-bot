import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import uuid
import os

TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)


# =========================
# تحميل الفيديو
# =========================
def download_video(url):
    file_id = str(uuid.uuid4())
    file_path = f"{DOWNLOAD_DIR}/{file_id}.mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": file_path,
        "noplaylist": True,
        "quiet": True,
        "geo_bypass": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return file_path


# =========================
# start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 بوت أبو كيان يرحب بك\n\n"
        "📥 أرسل رابط يوتيوب أو تيك توك\n"
        "⚡ وسيتم التحميل فوراً"
    )


# =========================
# handle messages
# =========================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "http" not in url:
        await update.message.reply_text("📌 أرسل رابط صحيح")
        return

    await update.message.reply_text("⚡ جاري التحميل...")

    try:
        file_path = download_video(url)

        with open(file_path, "rb") as f:
            await update.message.reply_video(
                f,
                caption="👑 تم التحميل بواسطة بوت أبو كيان"
            )

    except Exception as e:
        await update.message.reply_text(f"❌ فشل التحميل\n{e}")


# =========================
# تشغيل البوت
# =========================
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
