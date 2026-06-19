import os
import time
import urllib.parse
import requests
from io import BytesIO
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from downloader import download_video

# التوكن الخاص بك
TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # 1. قسم تحميل الفيديو
    if "tiktok.com" in text or "vm.tiktok" in text:
        file_name = f"video_{int(time.time())}.mp4"
        await update.message.reply_text("⏳ جاري تحميل الفيديو...")
        try:
            download_video(text, file_name)
            await update.message.reply_video(video=open(file_name, "rb"))
            os.remove(file_name)
        except Exception as e:
            await update.message.reply_text(f"خطأ في التحميل: {str(e)}")
            if os.path.exists(file_name): os.remove(file_name)
            
    # 2. قسم تصميم الصور (المعدل)
    else:
        prompt = f"{text}, cinematic style, 8k, high quality"
        encoded_text = urllib.parse.quote(prompt)
        # الرابط الجديد الأكثر استقراراً
        image_url = f"https://image.pollinations.ai/prompt/{encoded_text}?width=1024&height=1024&nologo=true&seed={int(time.time())}"
        
        await update.message.reply_text("🎨 جاري رسم تصميمك، لحظات...")
        try:
            # تحميل الصورة كملف حقيقي لحل مشكلة الشعار
            response = requests.get(image_url)
            if response.status_code == 200:
                await update.message.reply_photo(photo=BytesIO(response.content), caption="✅ تم التصميم بنجاح!")
            else:
                await update.message.reply_text("⚠️ الموقع مشغول، حاول مجدداً بعد ثوانٍ.")
        except Exception as e:
            await update.message.reply_text(f"خطأ: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل الآن بكامل طاقته...")
    app.run_polling()
