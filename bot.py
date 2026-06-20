import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from PIL import Image, ImageEnhance
import yt_dlp

TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# أمر البدء المخصص
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("أبو كيان يرحب بكم")

# تحميل فيديوهات تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    await message.answer("🔄 جاري المعالجة...")
    url = message.text
    ydl_opts = {'outtmpl': 'video.mp4', 'format': 'best'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await message.answer_video(types.FSInputFile("video.mp4"))
        if os.path.exists("video.mp4"): os.remove("video.mp4")
    except Exception as e:
        await message.answer("❌ تعذر تحميل الفيديو، تأكد من الرابط.")

# تعديل الصور بفلتر احترافي
@dp.message(F.photo)
async def process_photo(message: types.Message):
    photo_path = f"img_{message.from_user.id}.jpg"
    await bot.download(message.photo[-1], destination=photo_path)
    
    img = Image.open(photo_path)
    # فلتر ألوان الآيفون
    img = ImageEnhance.Color(img).enhance(1.3)
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img.save("filtered.jpg")
    
    await message.answer_photo(types.FSInputFile("filtered.jpg"), caption="✨ تم تطبيق فلتر الآيفون")
    
    if os.path.exists(photo_path): os.remove(photo_path)
    if os.path.exists("filtered.jpg"): os.remove("filtered.jpg")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
