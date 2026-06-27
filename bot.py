import telebot
import os

TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "جاري رفع جودة الفيديو وكسر حاجز الدقة...")
    
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open('input.mp4', 'wb') as new_file:
        new_file.write(downloaded_file)

    # هذا الأمر يستخدم تقنية 'tune film' لزيادة حدة التفاصيل بشكل سينمائي 
    # مع رفع الجودة (CRF 12) بدون تحميل زائد على المعالج
    cmd = "ffmpeg -y -i input.mp4 -vf 'unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=1.5' -c:v libx264 -crf 12 -tune film -preset fast -r 60 -c:a copy output.mp4"
    
    os.system(cmd)
    
    if os.path.exists('output.mp4'):
        with open('output.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
    else:
        bot.reply_to(message, "حدث خطأ في كسر الدقة، حاول مع فيديو أصغر.")

bot.infinity_polling()
