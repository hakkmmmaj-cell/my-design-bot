import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

BOT_TOKEN = "8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec"
GEMINI_API_KEY = "AQ.Ab8RN6KBE5aKTARvvvUuLdNiBae4T3UnfjOUBf4W-qkdeJP4QA"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("أهلاً، أرسل أي رسالة وسأرد عليك بالذكاء الاصطناعي.")

@dp.message()
async def chat(message: types.Message):
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"خطأ: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
