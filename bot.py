import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageEnhance, ImageFilter
import yt_dlp

# ضع التوكن الجديد هنا
TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- دالة الفلاتر الاحترافية ---
def get_photo_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 فلتر الأيفون الأساسي", callback_data="filter_iphone")],
        [InlineKeyboardButton(text="✨ إضاءة احترافية", callback_data="filter_bright")],
        [InlineKeyboardButton(text="💎 حدة 4K فائقة", callback_data="filter_hd")]
    ])

# --- معالجة الصور ---
@dp.callback_query(F.data.startswith("filter_"))
async def apply_filter(callback: types.CallbackQuery):
    await callback.answer("جاري المعالجة...")
    try:
        img = Image.open("user_photo.jpg")
        
        if callback.data == "filter_iphone":
            img = ImageEnhance.Contrast(img).enhance(1.2)
            img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
        elif callback.data == "filter_bright":
            img = ImageEnhance.Brightness(img).enhance(1.3)
        elif callback.data == "filter_hd":
            img = img.filter(ImageFilter.DETAIL).filter(ImageFilter.SHARPEN)

        img.save("processed.jpg")
        await callback.message.answer_photo(photo=types.FSInputFile("processed.jpg"), caption="تمت المعالجة بجودة عالية ✨ - بوت أبو كيان")
    except Exception as e:
        await callback.message.answer("حدث خطأ أثناء المعالجة. حاول إرسال الصورة مرة أخرى.")

# --- تحميل التيك توك (بأفضل إعدادات) ---
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    wait_msg = await message.answer("🔄 جاري التحميل...")
    try:
        ydl_opts = {'outtmpl': 'video.mp4', 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        await message.answer_video(video=types.FSInputFile("video.mp4"), caption="تم التحميل بواسطة بوت أبو كيان 🚀")
        await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
    except Exception:
        await message.answer("تعذر تحميل الفيديو، تأكد من الرابط.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, "user_photo.jpg")
    await message.answer("اختر نوع الفلتر:", reply_markup=get_photo_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
