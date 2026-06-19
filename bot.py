import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from downloader import download_video

TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    # 1. إنشاء اسم ملف فريد (يختلف في كل مرة حسب الوقت)
    file_name = f"video_{int(time.time())}.mp4"
    
    await update.message.reply_text("Downloading... please wait.")
    
    try:
        # 2. تحميل الفيديو بالاسم الجديد
        download_video(url, file_name)
        
        # 3. إرسال الملف الجديد
        await update.message.reply_video(video=open(file_name, "rb"))
        
        # 4. حذف الملف من السيرفر بعد الإرسال (مهم جداً حتى لا يمتلئ المجلد)
        os.remove(file_name)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
        # تنظيف في حال حدوث خطأ
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
