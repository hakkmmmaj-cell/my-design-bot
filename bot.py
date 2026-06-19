import time
import urllib.parse
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from downloader import download_video

# التوكن الخاص بك
TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # 1. إذا كان رابط تيك توك - يحمل الفيديو
    if "tiktok.com" in text or "vm.tiktok" in text:
        await update.message.reply_text("⏳ جاري التحميل...")
        # (باقي كود التحميل الخاص بك هنا)
            
    # 2. إذا كان نص - يصمم صورة (الكود الدوكي)
    else:
        # نص بسيط جداً بدون إضافات تعقد الموقع
        encoded_text = urllib.parse.quote(text)
        # رابط مباشر وسريع
        image_url = f"https://pollinations.ai/p/{encoded_text}?width=1024&height=1024&seed={int(time.time())}"
        
        await update.message.reply_text("🎨 جاري التصميم...")
        # إرسال كـ رابط مباشر (ليقوم التليجرام هو بمعالجته)
        await update.message.reply_photo(photo=image_url)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
