import telebot
import os
from telebot import TeleBot

# ضع التوكن الخاص بك هنا
TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw" 
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! البوت جاهز الآن بمعالجة فيديوهات بحدة عالية جداً ودقة طولية احترافية.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري المعالجة بحدة عالية... يرجى الانتظار قليلاً.")
    
    # تحميل الفيديو
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # معالجة الفيديو: 
    # 1. تغيير الحجم للطول (720x1280) 
    # 2. إضافة فلتر حدة قوي (unsharp) 
    # 3. ترميز احترافي (crf 15) و 120 إطاراً
    cmd = ("ffmpeg -i input.mp4 -vf 'scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=2.0' "
           "-c:v libx264 -crf 15 -preset slow -r 120 -c:a copy output.mp4")
    
    os.system(cmd)

    # إرسال الفيديو
    try:
        video = open('output.mp4', 'rb')
        bot.send_video(message.chat.id, video)
        video.close()
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء إرسال الفيديو: {e}")

print("البوت يعمل الآن بأقصى أداء...")
bot.infinity_polling()
