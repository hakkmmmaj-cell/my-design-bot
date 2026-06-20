import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageEnhance, ImageFilter
import yt_dlp

TOKEN = '8835938014:AAFBTNbOwxzPbpFtR6kWoVTcU2ofRbWke70'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# القائمة المحدثة بـ 3 فلاتر
def get_photo_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="تحسين حدة 4K", callback_data="filter_4k")],
        [InlineKeyboardButton(text="أبيض وأسود", callback_data="filter_bw")],
        [InlineKeyboardButton(text="تباين سينمائي", callback_data="filter_contrast")],
        [InlineKeyboardButton(text="فلتر التوهج", callback_data="filter_glow")]
    ])

@dp.message(F.photo)
async def photo_menu(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "user_photo.jpg")
    await message.answer("اختر نوع التعديل الذي تريده:", reply_markup=get_photo_menu())

@dp.callback_query(F.data.startswith("filter_"))
async def apply_filter(callback: types.CallbackQuery):
    img = Image.open("user_photo.jpg")
    filter_type = callback.data
    
    if filter_type == "filter_4k":
        img = ImageEnhance.Sharpness(img).enhance(4.0) # حدة قصوى
    elif filter_type == "filter_bw":
        img = img.convert("L")
    elif filter_type == "filter_contrast":
        img = ImageEnhance.Contrast(img).enhance(2.0)
    elif filter_type == "filter_glow":
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    img.save("result.jpg")
    await callback.message.answer_photo(photo=types.FSInputFile("result.jpg"), caption="تم التعديل بواسطة بوت أبو كيان ✨")

# (كود التيك توك يبقى كما هو)
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    await message.answer("جاري التحميل...")
    ydl_opts = {'outtmpl': 'video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([message.text])
    await message.answer_video(video=types.FSInputFile("video.mp4"), caption="تحميل بواسطة بوت أبو كيان")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
