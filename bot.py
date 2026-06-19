import logging
import os
from aiogram import Bot, Dispatcher, executor, types
import google.generativeai as genai

# تم وضع بياناتك هنا كما طلبت
TELEGRAM_TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'
GEMINI_API_KEY = 'AIzaSyCn4eCavPMFkvZVa5inn9lOniOXtuFXk3I'

# إعداد الخدمات
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("أهلاً بك! البوت يعمل الآن وبدأ يتصل بـ Gemini.")

@dp.message_handler()
async def chat_with_gemini(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        response = model.generate_content(message.text)
        await message.reply(response.text)
    except Exception as e:
        await message.reply("عذراً، حدث خطأ في الاتصال.")
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
