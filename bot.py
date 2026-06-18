from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from downloader import download_video

# ضع التوكن الجديد هنا بين علامتي التنصيص
TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل لي رابط فيديو وسأقوم بتحميله لك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("جاري التحميل... يرجى الانتظار.")
    
    try:
        # هنا نستدعي الدالة مع اسم الملف
        download_video(url, "video.mp4")
        await update.message.reply_video(video=open("video.mp4", "rb"))
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن...")
    application.run_polling()
