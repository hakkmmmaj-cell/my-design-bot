import os
import time
import urllib.parse
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
        await update.message.reply_text("⏳ جاري تحميل الفيديو، يرجى الانتظار...")
        try:
            download_video(text, file_name)
            await update.message.reply_video(video=open(file_name, "rb"))
            os.remove(file_name)
        except Exception as e:
            await update.message.reply_text(f"خطأ في التحميل: {str(e)}")
            if os.path.exists(file_name): os.remove(file_name)
            
    # 2. قسم تصميم الصور بالذكاء الاصطناعي (معدل لضمان الجودة)
    else:
        # إضافة وصف تقني لضمان خروج الصورة بشكل احترافي
        prompt = f"{text}, masterpiece, high quality, 8k, detailed, professional digital art"
        encoded_text = urllib.parse.quote(prompt)
        
        # استخدام موديل flux لنتائج أفضل وتجنب شعار الموقع
        image_url = f"https://pollinations.ai/p/{encoded_text}?width=1024&height=1024&nologo=true&model=flux&seed={int(time.time())}"
        
        await update.message.reply_text("🎨 جاري رسم تصميمك، لحظات...")
        try:
            # نرسل الصورة مع كابشن لإجبار التليجرام على المعالجة
            await update.message.reply_photo(photo=image_url, caption="✅ تم التصميم بواسطة الذكاء الاصطناعي")
        except Exception:
            await update.message.reply_text("⚠️ حدث خطأ في الاتصال بالموقع، حاول إرسال النص مرة أخرى.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل بكامل طاقته...")
    app.run_polling()
