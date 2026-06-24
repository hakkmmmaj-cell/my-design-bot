import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ضع التوكن الخاص بك هنا
TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل رابط الفيديو وسأقوم بتحميله لك.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    # رسالة انتظار
    status_msg = await update.message.reply_text("⏳ جاري المعالجة والتحميل... يرجى الانتظار")

    # إعدادات قوية لتجاوز حظر يوتيوب
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'downloads/{chat_id}.%(ext)s',
        'noplaylist': True,
        # هذا السطر يجعل السيرفر يتنكر كمتصفح حقيقي لتجاوز حظر يوتيوب
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # إرسال الفيديو للمستخدم
        await update.message.reply_video(video=open(filename, 'rb'))
        
        # حذف الملف بعد الإرسال
        os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ: {str(e)}\nربما الفيديو خاص أو محظور إقليمياً.")

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    app.run_polling()
