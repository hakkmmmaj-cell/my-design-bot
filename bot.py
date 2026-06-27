import telebot
import os
import subprocess

TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري المعالجة الاحترافية... انتظر.")
    
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # استخدام المسارات المباشرة
    input_path = "input.mp4"
    output_path = "output.mp4"
    
    with open(input_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # هذا الأمر سيجبر النظام على معالجة الفيديو برفع الحادة وتغيير الـ Bitrate
    # نستخدم subprocess للتأكد من أن الأمر يعمل فعلياً
    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', 'unsharp=luma_msize_x=7:luma_msize_y=7:luma_amount=3.0,hqdn3d',
        '-c:v', 'libx264', '-crf', '18', '-preset', 'ultrafast',
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True)
        if os.path.exists(output_path):
            with open(output_path, 'rb') as video:
                bot.send_video(message.chat.id, video)
        else:
            bot.reply_to(message, "فشلت المعالجة: لم يتم إنشاء الفيديو.")
    except Exception as e:
        bot.reply_to(message, f"خطأ برمجي: {str(e)}")

bot.infinity_polling()
