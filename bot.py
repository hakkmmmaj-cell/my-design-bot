import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي أي رابط من يوتيوب أو تيك توك وسأقوم بتحميله لك بجودة عالية.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    
    await update.message.reply_text("⏳ جاري المعالجة... يرجى الانتظار")

    # إعدادات yt-dlp القوية للتحميل
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # اختيار أفضل جودة
        'outtmpl': f'downloads/{chat_id}.%(ext)s', # حفظ الفيديو برقم المستخدم
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # إرسال الفيديو للمستخدم
        await update.message.reply_video(video=open(filename, 'rb'))
        
        # حذف الملف من السيرفر بعد الإرسال لتوفير المساحة
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}")

# إعداد التطبيق
if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("البوت يعمل الآن...")
    app.run_polling()
