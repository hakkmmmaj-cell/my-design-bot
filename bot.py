import telebot
import os

# ضع التوكن الخاص بك بين علامتي التنصيص هنا مباشرة
TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw" 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "تم تفعيل البوت. أرسل الفيديو الآن.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري المعالجة...")
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)
    
    cmd = "ffmpeg -i input.mp4 -vf scale=1920:1080:flags=lanczos,unsharp=7:7:2.5:7:7:2.5 -c:v libx264 -crf 10 -preset slow -r 120 -c:a copy output.mp4"
    os.system(cmd)
    
    with open('output.mp4', 'rb') as video:
        bot.send_video(message.chat.id, video)

bot.infinity_polling()
