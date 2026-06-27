import telebot
import os

TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري تطبيق فلاتر الحدة...")
    
    # تنظيف الملفات القديمة
    if os.path.exists('input.mp4'): os.remove('input.mp4')
    if os.path.exists('output.mp4'): os.remove('output.mp4')
    
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # استخدام فلاتر قياسية ومضمونة 100%
    # luma_amount=3.0 تعطي حدة قوية جداً
    cmd = "ffmpeg -y -i input.mp4 -vf 'hqdn3d,unsharp=5:5:3.0:5:5:3.0' -c:v libx264 -crf 15 -preset ultrafast -c:a copy output.mp4"
    os.system(cmd)
    
    # إرسال الملف الناتج فقط
    if os.path.exists('output.mp4'):
        with open('output.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
    else:
        bot.reply_to(message, "فشل تطبيق الفلاتر.")

bot.infinity_polling()
