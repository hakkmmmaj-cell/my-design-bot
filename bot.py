import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# تم وضع بياناتك هنا كما طلبت
TELEGRAM_TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'
GEMINI_API_KEY = 'AIzaSyCn4eCavPMFkvZVa5inn9lOniOXtuFXk3I'

# إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# إعداد البوت
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("أهلاً! البوت يعمل الآن بشكل ممتاز على Railway.")

@dp.message()
async def chat(message: types.Message):
    # إرسال حالة "جاري الكتابة"
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer("عذراً، حدث خطأ أثناء الاتصال بالذكاء الاصطناعي.")
        logging.error(f"Error: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
