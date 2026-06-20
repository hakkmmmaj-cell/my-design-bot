import asyncio
import yt_dlp
import cv2
import numpy as np
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# 1. إعدادات البوت
TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec' # <-- ضع التوكن الخاص بك هنا
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 2. دالة التصميم السينمائي
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

# 3. معالجة الروابط (تيك توك)
@dp.message(F.text.contains("tiktok.com"))
async def handle_tiktok(message: types.Message):
    await message.answer("📥 جاري تحميل الفيديو من تيك توك، انتظر...")
    ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        await message.answer_video(video=FSInputFile("video.mp4"), caption="تم التحميل بواسطة بوت أبو كيان ✨")
    except Exception as e:
        await message.answer(f"حدث خطأ أثناء التحميل: {e}")

# 4. معالجة الصور (تصميم سينمائي)
@dp.message(F
