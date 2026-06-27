import telebot
import os
import time  # أضفنا مكتبة الوقت

TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري المعالجة الاحترافية... انتظر قليلاً.")
    
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # معالجة الفيديو
    cmd = "ffmpeg -y -i input.mp4 -vf scale=1920:1080:flags=lanczos,unsharp=7:7:2.5:7:7:2.5 -c:v libx264 -crf 10 -preset slow -r 120 -c:a copy output.mp4"
    os.system(cmd)
    
    # تأكد أن الفيديو موجود قبل الإرسال
    if os.path.exists('output.mp4'):
        with open('output.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
    else:
        bot.reply_to(message, "فشلت المعالجة، يرجى المحاولة مرة أخرى.")

bot.infinity_polling()
