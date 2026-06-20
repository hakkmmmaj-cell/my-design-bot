import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import yt_dlp
from PIL import Image, ImageEnhance
import os

TOKEN = '8835938014:AAFBTNbOwxzPbpFtR6kWoVTcU2ofRbWke70'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# الترحيب مع الحقوق العربية
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "أهلاً بك في بوت أبو كيان! 🚀\n"
        "أنا هنا لمساعدتك في تحميل فيديوهات تيك توك وتعديل صورك.\n\n"
        "--------------------------\n"
        "مبرمج البوت: أبو كيان © 2026"
    )

# تحميل تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def tiktok_dl(message: types.Message):
    await message.answer("جاري جلب الفيديو من تيك توك...")
    ydl_opts = {'outtmpl': 'video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([message.text])
    await message.answer_video(video=types.FSInputFile("video.mp4"), caption="تم التحميل بواسطة بوت أبو كيان")

# تحسين دقة الصورة (فلتر بسيط)
@dp.message(F.photo)
async def photo_process(message: types.Message):
    await message.answer("جاري تحسين دقة الصورة...")
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "photo.jpg")
    
    img = Image.open("photo.jpg")
    img = img.convert("RGB")
    # تحسين الحدة والتباين لتبدو أوضح
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.5)
    img.save("result.jpg")
    
    await message.answer_photo(photo=types.FSInputFile("result.jpg"), caption="تم تحسين الصورة - بوت أبو كيان")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
