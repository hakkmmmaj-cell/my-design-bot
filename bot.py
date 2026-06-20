import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from PIL import Image, ImageEnhance, ImageFilter
import asyncio
import os

# ضع توكن البوت الخاص بك هنا
TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً بك! أرسل لي صورة وسأقوم بتحسينها أو إضافة فلاتر عليها.")

@dp.message(F.photo)
async def process_photo(message: types.Message):
    # تحميل الصورة من تليجرام
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    # حفظ الصورة مؤقتاً
    await bot.download_file(file_path, "temp.jpg")
    
    # معالجة الصورة (تحسين التباين)
    img = Image.open("temp.jpg")
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    img.save("processed.jpg")
    
    # إرسال الصورة المعالجة
    await message.answer_photo(photo=types.FSInputFile("processed.jpg"), caption="تم تحسين الصورة.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
