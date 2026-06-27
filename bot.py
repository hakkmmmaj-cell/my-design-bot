import telebot
import os

# ضع التوكن الخاص بك مباشرة هنا بين علامتي التنصيص
TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw" 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك! أنا بوت تصميم الفيديوهات. أرسل لي الفيديو وسأقوم بتعديله إلى 120 إطاراً في الثانية.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري معالجة الفيديو، يرجى الانتظار...")
    
    # تحميل الفيديو
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # معالجة الفيديو بـ ffmpeg إلى 120 إطاراً
    # تم حذف شرط القناة، التعديل يتم مباشرة
    os.system("ffmpeg -i input.mp4 -r 120 -c:a copy output.mp4")

    # إرسال الفيديو المعدل
    try:
        video = open('output.mp4', 'rb')
        bot.send_video(message.chat.id, video)
        video.close()
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء إرسال الفيديو: {e}")

print("البوت يعمل الآن...")
bot.infinity_polling()
