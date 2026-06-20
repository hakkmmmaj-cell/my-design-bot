import os
import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# 1. إعداد السجلات (لتعرف ليش البوت يطفي لو صار خطأ)
logging.basicConfig(level=logging.INFO)

# 2. جلب المفاتيح من السيرفر (لا تغير شيء هنا)
TOKEN = os.getenv('8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8')

# 3. تفعيل البوت والذكاء الاصطناعي
bot = Bot(token=TOKEN)
dp = Dispatcher()
genai.configure(api_key=AI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. رسالة الترحيب بـ "أبو كيان"
@dp.message(Command("start"))
async def welcome(message: types.Message):
    await message.answer("هلا والله يا بطل! 👋\nأنا بوت أبو كيان، مساعدك الذكي والمبرمج. أنا هنا لخدمتك!")

# 5. الرد الذكي (AI)
@dp.message()
async def handle_ai_chat(message: types.Message):
    # نتحقق إذا الرسالة مو رابط تيك توك عشان يرد عليها الذكاء الاصطناعي
    if "tiktok.com" not in message.text:
        await message.answer("🤖 جاري التفكير...")
        try:
            response = model.generate_content(message.text)
            await message.answer(response.text)
        except Exception as e:
            await message.answer("حدث خطأ في الذكاء الاصطناعي، تأكد من مفتاح الـ API.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
