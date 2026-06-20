import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageEnhance, ImageFilter
import yt_dlp

# اترك هذا المكان فارغاً وضع التوكن الجديد الخاص بك هنا
TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8' 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# القائمة (بدون روابط خارجية)
def get_photo_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="تحسين حدة 4K (عالية جداً)", callback_data="filter_4k")],
        [InlineKeyboardButton(text="أبيض وأسود", callback_data="filter_bw")]
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً بك في بوت أبو كيان الخاص بك! أرسل صورة للبدء أو رابط تيك توك. © 2026")

# معالجة الصور بحدة عالية
@dp.callback_query(F.data == "filter_4k")
async def enhance_4k(callback: types.CallbackQuery):
    img = Image.open("user_photo.jpg")
    # تقنية تحسين الحدة العالية
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=300, threshold=3))
    img.save("processed.jpg")
    await callback.message.answer_photo(photo=types.FSInputFile("processed.jpg"), caption="تم تحسين حدة الصورة بدقة عالية - بوت أبو كيان")

# كود التيك توك (بدون قيود)
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    await message.answer("جاري التحميل...")
    ydl_opts = {'outtmpl': 'video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([message.text])
    await message.answer_video(video=types.FSInputFile("video.mp4"), caption="تم التحميل بواسطة بوت أبو كيان")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "user_photo.jpg")
    await message.answer("تم استلام الصورة، اختر التحسين:", reply_markup=get_photo_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
