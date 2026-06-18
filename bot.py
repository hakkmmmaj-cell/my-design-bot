from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from downloader import download_video

# التوكن (ضعه هنا مؤقتاً بعد الحصول على واحد جديد من BotFather)
TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    # هنا حددنا اسم الملف ليتم إرساله للدالة
    filename = "video.mp4" 
    
    await update.message.reply_text("جاري التحميل، يرجى الانتظار
