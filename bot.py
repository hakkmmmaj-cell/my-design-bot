import asyncio
import yt_dlp
import cv2
import numpy as np
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# إعداد البوت
TOKEN = '8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc' 
bot = Bot(token=TOKEN)
dp = Dispatcher()

# دالة الفلتر السينمائي
def apply_cinematic_filter(image_path, output_path):
    img = cv2.imread(image_path)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    img = cv2.cvtColor(cv2.merge((cl,a,b)), cv2.COLOR_LAB2BGR)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(output_path, img)

# أمر البدء
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً بك في بوت 『أبـو كـيـان』 للتحميل والتصميم السينمائي! ✨\nأرسل رابط تيك توك للتحميل، أو أرسل صورة لتطبيق الفلتر.")

# تحميل فيديو تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def handle_tiktok(message: types.Message):
    msg = await message.answer("📥 جاري تحميل الفيديو من تيك توك، انتظر...")
    ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        await message.answer_video(video=FSInputFile("video.mp4"), caption="تم التحميل بواسطة بوت أبو كيان ✨")
        os.remove("video.mp4")
        await msg.delete()
    except Exception as e:
        await message.answer(f"حدث خطأ: {e}")

# معالجة الصور
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("🎨 جاري تطبيق الفلتر السينمائي...")
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "input.jpg")
    
    apply_cinematic_filter("input.jpg", "output.jpg")
    
    await message.answer_photo(photo=FSInputFile("output.jpg"), caption="التصميم السينمائي من 『أبـو كـيـان』✨")
    os.remove("input.jpg")
    os.remove("output.jpg")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
