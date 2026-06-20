import os
import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# تفعيل السجلات
logging.basicConfig(level=logging.INFO)

# جلب المتغيرات
TOKEN = os.getenv('8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8')
API_K
# سطر للتأكد فقط (هذا سيظهر في الـ Logs في Railway لنتأكد هل المتغير فارغ أم لا)
print(f"DEBUG: Token is {'Present' if TOKEN else 'MISSING'}")

# إعداد البوت
bot = Bot(token=TOKEN)
dp = Dispatcher()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@dp.message(Command("start"))
async def welcome(message: types.Message):
    await message.answer("أهلاً بك يا أبو كيان، أنا أعمل الآن!")

@dp.message()
async def chat_with_ai(message: types.Message):
    if not message.text: return
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer("حدث خطأ في الاتصال بالذكاء الاصطناعي.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
