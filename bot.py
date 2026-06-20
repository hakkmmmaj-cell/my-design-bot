import os
import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# تفعيل تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# 1. جلب المفاتيح من المتغيرات في Railway (لا تضع التوكن هنا!)
TOKEN = os.getenv('TOKEN')
API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد البوت والذكاء الاصطناعي
bot = Bot(token=TOKEN)
dp = Dispatcher()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# رسالة الترحيب
@dp.message(Command("start"))
async def welcome(message: types.Message):
    await message.answer("هلا والله يا بطل! 👋\nأنا بوت أبو كيان الذكي، كيف أقدر أساعدك اليوم؟")

# الرد الذكي
@dp.message()
async def chat_with_ai(message: types.Message):
    if not message.text:
        return
    
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer("حدث خطأ تقني، تأكد من إعدادات المفاتيح في Railway.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
