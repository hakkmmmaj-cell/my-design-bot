
2.  **وهذا هو الكود المطور لملف `bot.py`:**

```python
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from PIL import Image, ImageEnhance
import yt_dlp
import os

TOKEN = '8835938014:AAFBTNbOwxzPbpFtR6kWoVTcU2ofRbWke70'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. أمر الترحيب
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً بك يا أبو كيان! أرسل لي رابط تيك توك للتحميل، أو صورة لأقوم بتحسينها.")

# 2. تحميل فيديوهات تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    await message.answer("جاري التحميل... يرجى الانتظار.")
    ydl_opts = {'outtmpl': 'video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([message.text])
    await message.answer_video(video=types.FSInputFile("video.mp4"), caption="تم التحميل بواسطة أبو كيان")

# 3. تحسين دقة الصورة (فلتر بسيط)
@dp.message(F.photo)
async def process_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "photo.jpg")
    
    img = Image.open("photo.jpg")
    enhancer = ImageEnhance.Sharpness(img) # تحسين الحدة
    img = enhancer.enhance(2.0)
    img.save("result.jpg")
    
    await message.answer_photo(photo=types.FSInputFile("result.jpg"), caption="تم تحسين الصورة - أبو كيان")

import asyncio
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
