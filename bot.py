import os
import telebot

# جرب وضع التوكن مباشرة هنا بين علامات التنصيص لتختبر التشغيل
TOKEN = "8609342978:AAGdvzdShxfhyEoOM_ob1k9_fT9mZs-QPOw" 

# إذا كنت لا تزال تريد استخدام المتغيرات، تأكد أنها موجودة كما في الخطوة 1
# TOKEN = os.environ.get('BOT_TOKEN') 

bot = telebot.TeleBot(TOKEN)
