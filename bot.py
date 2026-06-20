import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

TOKEN = '8835938014:AAFBTNbOwxzPbpFtR6kWoVTcU2ofRbWke70'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# أزرار الصور
def get_photo_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="تحسين دقة الصورة (4K)", callback_data="enhance_4k")],
        [InlineKeyboardButton(text="فلتر سينمائي", callback_data="apply_filter")]
    ])

# 1. الترحيب
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً بك في بوت أبو كيان! أرسل رابط تيك توك للتحميل، أو أرسل صورة للتحسين.\n\n© 2026 أبو كيان")

# 2. تحميل تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    await message.answer("جاري تحميل الفيديو، يرجى الانتظار...")
    ydl_opts = {'outtmpl': 'video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([message.text])
    await message.answer_video(video=types.FSInputFile("video.mp4"), caption="تم التحميل بواسطة بوت أبو كيان")

# 3. استلام الصور وإظهار الأزرار
@dp.message(F.photo)
async def photo_menu(message: types.Message):
    await message.answer("تم استلام الصورة! اختر نوع التعديل:", reply_markup=get_photo_menu())

# 4. تنفيذ أوامر الأزرار
@dp.callback_query(F.data.in_({"enhance_4k", "apply_filter"}))
async def handle_buttons(callback: types.CallbackQuery):
    action = "تحسين الدقة" if callback.data == "enhance_4k" else "تطبيق الفلتر"
    await callback.message.answer(f"جاري {action}.. هذه الميزة تحتاج معالجة سيرفر خاصة - بوت أبو كيان")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
