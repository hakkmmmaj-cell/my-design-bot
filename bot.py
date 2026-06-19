import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import google.generativeai as genai

# استخدم مفتاح Gemini المجاني الخاص بك
API_KEY = 'AQ.Ab8RN6KBE5aKTARvvvUuLdNiBae4T3UnfjOUBf4W-qkdeJP4QA' # (تأكد أن هذا المفتاح من Google AI Studio)
TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'

genai.configure(api_key=API_KEY)
# استخدام نموذج Imagen المخصص للصور
model = genai.GenerativeModel('imagen-3.0-generate-001')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def generate_image(message):
    await message.answer("جاري التصميم بواسطة جوجل، يرجى الانتظار...")
    try:
        # طلب توليد صورة
        result = model.generate_content(message.text)
        await message.answer(result.text) # سيعطيك رابط الصورة أو النتيجة
    except Exception as e:
        await message.answer(f"تعذر التصميم: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
