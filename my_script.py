from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image, ImageEnhance
import os

TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'

async def handle_photo(update, context):
    file = await update.message.photo[-1].get_file()
    await file.download_to_drive("in.jpg")
    
    img = Image.open("in.jpg")
    # تطبيق فلتر سينمائي (تباين وتشبع)
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Color(img).enhance(1.3)
    img.save("out.jpg")
    
    await update.message.reply_photo(photo=open("out.jpg", 'rb'), caption="تمت المعالجة سينمائياً!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("البوت يعمل الآن..")
    app.run_polling()
