import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ضع التوكن الخاص بك هنا فقط
BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك في بوت أبو كيان! أرسل رابط تيك توك وسأحمله لك.")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        return

    status = await update.message.reply_text("📥 جاري التحميل...")
    file_name = "video.mp4"
    
    ydl_opts = {'outtmpl': file_name}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        await update.message.reply_video(
            video=open(file_name, 'rb'),
            caption="تم التحميل بواسطة بوت أبو كيان ⚡️"
        )
        await status.delete()
    except Exception as e:
        await status.edit_text(f"❌ حدث خطأ: {e}")
    
    if os.path.exists(file_name):
        os.remove(file_name)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    app.run_polling()
