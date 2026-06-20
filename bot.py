import os
# هذا السطر سيجبر السيرفر على تحميل المكتبات قبل أي شيء آخر
os.system("pip install moviepy aiogram google-generativeai")

import asyncio
from aiogram import Bot, Dispatcher, types
import google.generativeai as genai

# التوكن الجديد (الذي استخرجته من BotFather)
TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# إعداد مفتاح جيمناي
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@dp.message()
async def chat(message: types.Message):
    response = model.generate_content(message.text)
    await message.answer(response.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
