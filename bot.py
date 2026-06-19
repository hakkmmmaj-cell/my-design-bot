import urllib.parse
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"

async def generate_design(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # تحويل النص إلى صيغة يفهمها الرابط
    encoded_text = urllib.parse.quote(user_text)
    
    # رابط خدمة Pollinations المجانية لتوليد الصور
    # نقوم بإضافة الوقت (time) لضمان أن الصورة تتغير في كل مرة
    image_url = f"https://pollinations.ai/p/{encoded_text}?width=1024&height=1024&seed=42"
    
    await update.message.reply_text("جاري التصميم بواسطة الذكاء الاصطناعي...")
    
    try:
        # إرسال الصورة
        await update.message.reply_photo(photo=image_url)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_design))
    app.run_polling()
