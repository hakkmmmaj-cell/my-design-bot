import os
import sys
import subprocess

# 1. تثبيت المكتبات فوراً وقبل استيراد أي شيء
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import aiogram
    import google.generativeai
    import moviepy
except ImportError:
    install("aiogram")
    install("google-generativeai")
    install("moviepy")

# 2. الآن استورد المكتبات بعد أن تأكدنا من تثبيتها
import asyncio
from aiogram import Bot, Dispatcher, types
import google.generativeai as genai

# التوكن الجديد
TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# إعداد Gemini
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
