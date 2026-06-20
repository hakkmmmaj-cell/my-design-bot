import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from PIL import Image, ImageEnhance, ImageFilter
import yt_dlp

TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. تحميل فيديو تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    await message.answer("🔄 جاري تحميل الفيديو من تيك توك، انتظر قليلاً...")
    url = message.text
    ydl_opts = {'outtmpl': 'video.mp4', 'format': 'best'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await message.answer_video(types.FSInputFile("video.mp4"))
        os.remove("video.mp4")
    except Exception as e:
        await message.answer(f"❌ حدث خطأ أثناء التحميل: {e}")

# 2. تعديل الصور (فلاتر احترافية)
@dp.message(F.photo)
async def process_photo(message: types.Message):
    photo_path = f"photo_{message.from_user.id}.jpg"
    await bot.download(message.photo[-1], destination=photo_path)
    
    # تطبيق فلتر "ايفون" (زيادة التباين والتشبع)
    img = Image.open(photo_path)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3) # تشبع ألوان
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2) # تباين
    img.save("filtered.jpg")
    
    await message.answer_photo(types.FSInputFile("filtered.jpg"), caption="✨ تم تطبيق فلتر الألوان الاحترافي")
    
    # تنظيف الملفات
    os.remove(photo_path)
    os.remove("filtered.jpg")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
 
