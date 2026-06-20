import os
import asyncio
from aiogram import Bot, Dispatcher, types
import google.generativeai as genai

# هذا التوكن الخاص بك، لا تضع علامات تنصيص إضافية
TOKEN = "8835938014:AAEE7yIeXt7K3EkUUmxUyI4vAt5O4_Q"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# إعداد مفتاح جيمناي من الـ Variables
gemini_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@dp.message()
async def chat_handler(message: types.Message):
    if not message.text:
        return
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer("حدث خطأ في الرد، تأكد من مفتاح Gemini في الـ Variables.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
