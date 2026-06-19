import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# توكن البوت
TELEGRAM_TOKEN = "ضع_توكن_البوت_هنا"

# مفتاح Gemini
GEMINI_API_KEY = "ضع_مفتاح_Gemini_هنا"

# إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# إعداد البوت
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("🤖 أهلاً بك، البوت يعمل بنجاح!")

@dp.message()
async def chat(message: types.Message):
    try:
        await bot.send_chat_action(message.chat.id, "typing")

        response = model.generate_content(message.text)

        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("لم يتم توليد رد.")

    except Exception as e:
        await message.answer(f"❌ خطأ:\n{e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
