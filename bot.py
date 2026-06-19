import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from downloader import download_video

# إعداد السجل (Logging) مهم جداً للاستضافة لمعرفة الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    # نستخدم نصاً إنجليزياً لتجنب مشاكل الترميز في Railway
    await update.message.reply_text("Downloading... please wait.")
    try:
        download_video(url, "video.mp4")
        await update.message.reply_video(video=open("video.mp4", "rb"))
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
