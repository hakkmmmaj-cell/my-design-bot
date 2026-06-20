import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageEnhance
import yt_dlp
import os

TOKEN = '8835938014:AAFBTNbOwxzPbpFtR6kWoVTcU2ofRbWke70'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# القائمة التفاعلية للصور
def get_photo_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="تحسين دقة الصورة (4K)", callback_data="enhance_4k")],
        [InlineKeyboardButton(text="فلتر سينمائي", callback_data="apply_filter")]
    ])

# 1. الترحيب
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً بك يا أبو كيان! أرسل رابط تيك توك للتحميل، أو صورة لأقوم بتعديلها.\n© 2026 أبو كيان")

# 2. تحميل تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    status = await message.answer("جاري تحميل الفيديو من تيك توك...")
    ydl_opts = {'outtmpl': 'video.mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        await message.answer_video(video=types.FSInputFile("video.mp4"), caption="تم التحميل بواسطة بوت أبو كيان")
    except Exception as e:
        await message.answer("حدث خطأ أثناء التحميل، تأكد من الرابط.")
    finally:
        await bot.delete_message(chat_id=message.chat.id, message_id=status.message_id)

# 3. معالجة الصور
@dp.message(F.photo)
async def photo_menu(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "user_photo.jpg")
    await message.answer("تم استلام الصورة، اختر التعديل:", reply_markup=get_photo_menu())

@dp.callback_query(F.data == "enhance_4k")
async def enhance_4k(callback: types.CallbackQuery):
    img = Image.open("user_photo.jpg")
    img = ImageEnhance.Sharpness(img).enhance(3.0)
    img.save("processed.jpg")
    await callback.message.answer_photo(photo=types.FSInputFile("processed.jpg"), caption="تم تحسين الدقة - بوت أبو كيان")

@dp.callback_query(F.data == "apply_filter")
async def apply_filter(callback: types.CallbackQuery):
    img = Image.open("user_photo.jpg").convert("L")
    img.save("processed.jpg")
    await callback.message.answer_photo(photo=types.FSInputFile("processed.jpg"), caption="تم تطبيق الفلتر السينمائي - بوت أبو كيان")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
