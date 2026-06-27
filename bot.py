import telebot
import os

# هذا الكود سيقرأ التوكن من المتغيرات في Railway تلقائياً
TOKEN = os.environ.get('8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "تم تفعيل البوت بأقصى إعدادات الجودة والحدة. أرسل الفيديو الآن!")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري معالجة الفيديو بجودة احترافية (Upscale & Sharpen)...")
    
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # أمر المعالجة "الوحشي" لرفع الدقة والحدة إلى أقصى حد
    cmd = ("ffmpeg -i input.mp4 -vf 'scale=1920:1080:flags=lanczos,unsharp=7:7:2.5:7
