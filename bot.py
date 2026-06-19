import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import google.generativeai as genai

# ضع التوكن الجديد الذي أخذته من BotFather هنا
TELEGRAM_TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'

# ضع مفتاح Gemini الجديد هنا
GEMINI_API_KEY = 'AQ.Ab8RN6LYjt2jqli9obhxvjst5-v8AcoCnEOyX17s5_vnwhC2Ow'

# إعدادات الخدمة
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message):
    await message.answer("أهلاً! البوت متصل ويعمل الآن.")

@dp.message()
async def chat(message):
    # إظهار حالة جاري الكتابة
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"خطأ في الاتصال: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
