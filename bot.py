import os
import asyncio
from aiogram import Bot, Dispatcher, types
import google.generativeai as genai
TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyI4vAt5O4_Q'

# إعداد التوكن (مباشر لأننا جربناه واشتغل)
TOKEN = ''8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8" 
bot = Bot(token=TOKEN)
dp = Dispatcher()

# إعداد مفتاح جيمناي (يسحب من الـ Variables اللي ضفناها في Railway)
# تأكد أن اسم المتغير في Railway هو بالضبط: GEMINI_API_KEY
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
        await message.answer(f"صار خطأ: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
