import telebot
import os
from telebot import TeleBot

# ضع التوكن الخاص بك هنا
TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw" 
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي الفيديو، وسأقوم بمعالجته بدقة 720p و 120fps.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري المعالجة... يرجى الانتظار.")
    
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # هذا الأمر يقوم بتغيير الدقة إلى 720p ورفع الإطارات إلى 120fps
    os.system("ffmpeg -i input.mp4 -vf scale=1280:720 -r 120 -c:a copy output.mp4")

    try:
        video = open('output.mp4', 'rb')
        bot.send_video(message.chat.id, video)
        video.close()
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {e}")

bot.infinity_polling()
