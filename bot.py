import os
import time
import urllib.parse
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from downloader import download_video

TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # 1. إذا كانت الرسالة رابط (تحميل فيديو)
    if "tiktok.com" in text or "vm.tiktok" in text:
        file_name = f"video_{int(time.time())}.mp4"
        await update.message.reply_text("⏳ جاري تحميل الفيديو من تيك توك...")
        try:
            download_video(text, file_name)
            await update.message.reply_video(video=open(file_name, "rb"))
            os.remove(file_name)
        except Exception as e:
            await update.message.reply_text(f"خطأ في التحميل: {str(e)}")
            if os.path.exists(file_name): os.remove(file_name)
            
    # 2. إذا كانت الرسالة نص (تصميم ذكاء اصطناعي)
    else:
        encoded_text = urllib.parse.quote(text)
        image_url = f"https://pollinations.ai/p/{encoded_text}?width=1024&height=1024&nologo=true"
        await update.message.reply_text("🎨 جاري توليد التصميم، انتظر قليلاً...")
        try:
            await update.message.reply_photo(photo=image_url, caption="تصميمك جاهز!")
        except Exception as e:
            await update.message.reply_text(f"حدث خطأ في التصميم: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل الآن...")
    app.run_polling()
