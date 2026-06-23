import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# 🔐 ضع توكن البوت هنا
BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

# 🔑 ضع مفتاح Gemini هنا
GEMINI_API_KEY = "AQ.Ab8RN6I0i1dOOazZ6go_RRBhJ9Ps5T-tOZF8YiM58axOP2j0Dw"

# تهيئة Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# تشغيل البوت
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🚀 أمر البداية
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🤖 أهلاً بك!\n"
        "أرسل أي سؤال وأنا أجاوبك باستخدام الذكاء الاصطناعي."
    )

# 💬 الرد على الرسائل
@dp.message()
async def chat(message: types.Message):
    try:
        user_text = message.text

        response = model.generate_content(user_text)
        await message.answer(response.text)

    except Exception:
        await message.answer("⚠️ صار خطأ، حاول مرة ثانية")

# ▶️ تشغيل البوت
async def main():
    print("AI Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
