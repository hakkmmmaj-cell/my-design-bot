from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

# 🔴 توكن البوت
BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"


# 🎯 تحميل الفيديو
def download_video(url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "video.mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 بوت ابو كيان يرحب بك\n\n"
        "👋 أهلاً بيك!\n"
        "📥 ارسل رابط يوتيوب أو تيك توك وأنا أحمله لك"
    )


# 💬 استقبال الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # إذا رابط
    if "http" in text:
        await update.message.reply_text("⏳ جاري التحميل...")

        try:
            download_video(text)

            with open("video.mp4", "rb") as video:
                await update.message.reply_video(video)

        except Exception as e:
            print("ERROR:", e)
            await update.message.reply_text("❌ صار خطأ بالتحميل")

    else:
        await update.message.reply_text(
            "📌 ارسل رابط فقط (يوتيوب / تيك توك)"
        )


# ▶️ تشغيل البوت
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
