import telebot
import os
from telebot import TeleBot

# ضع التوكن الخاص بك هنا
TOKEN = os.environ.get('8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw')
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # تم حذف شرط القناة، الآن يرحب البوت بالمستخدم مباشرة
    bot.reply_to(message, "أهلاً بك! أرسل الفيديو الذي تريد تعديل إطاراته إلى 120fps.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري معالجة الفيديو، يرجى الانتظار...")
    
    # تحميل الفيديو
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # أمر ffmpeg لتعديل الإطارات إلى 120
    # نستخدم -r 120 لضبط عدد الإطارات في الثانية
    os.system("ffmpeg -i input.mp4 -r 120 -c:a copy output.mp4")

    # إرسال الفيديو المعدل
    video = open('output.mp4', 'rb')
    bot.send_video(message.chat.id, video)
    video.close()

bot.infinity_polling()
