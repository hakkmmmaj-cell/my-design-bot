import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

SERVER = "http://YOUR-SERVER-URL/download"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 بوت ابو كيان\n\nارسل رابط يوتيوب أو تيك توك"
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "http" not in url:
        await update.message.reply_text("📌 ارسل رابط فقط")
        return

    await update.message.reply_text("⚡ جاري التحميل...")

    try:
        r = requests.get(f"{SERVER}?url={url}&type=video")

        if r.status_code == 200:
            with open("file.mp4", "wb") as f:
                f.write(r.content)

            with open("file.mp4", "rb") as f:
                await update.message.reply_video(f)
        else:
            await update.message.reply_text("❌ فشل التحميل")

    except:
        await update.message.reply_text("❌ خطأ بالسيرفر")


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
