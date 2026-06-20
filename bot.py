import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageEnhance, ImageFilter
import yt_dlp

TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8' # ضع توكن البوت الجديد هنا
bot = Bot(token=TOKEN)
dp = Dispatcher()

# قائمة فلاتر الأيفون المخصصة
def get_photo_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="فلتر الأيفون الأساسي (iPhone Look)", callback_data="filter_iphone")],
        [InlineKeyboardButton(text="فلتر الإضاءة العالية (Bright Skin)", callback_data="filter_bright")],
        [InlineKeyboardButton(text="فلتر حدة التفاصيل (HD Detail)", callback_data="filter_hd")]
    ])

@dp.callback_query(F.data.startswith("filter_"))
async def apply_filter(callback: types.CallbackQuery):
    img = Image.open("user_photo.jpg")
    filter_type = callback.data
    
    if filter_type == "filter_iphone":
        # تباين أيفون احترافي
        img = ImageEnhance.Contrast(img).enhance(1.2)
        img = ImageEnhance.Color(img).enhance(1.1)
        img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=2))
        
    elif filter_type == "filter_bright":
        # إضاءة عالية (تأثير بشرة ناعمة)
        img = ImageEnhance.Brightness(img).enhance(1.2)
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
    elif filter_type == "filter_hd":
        # حدة تفاصيل قصوى
        img = img.filter(ImageFilter.SHARPEN)
        img = ImageEnhance.Contrast(img).enhance(1.3)

    img.save("processed.jpg")
    await callback.message.answer_photo(photo=types.FSInputFile("processed.jpg"), caption="تم التعديل بفلتر الأيفون - بوت أبو كيان ✨")

# كود التيك توك كما هو
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    await message.answer("جاري تحميل الفيديو...")
    ydl_opts = {'outtmpl': 'video.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([message.text])
    await message.answer_video(video=types.FSInputFile("video.mp4"), caption="تحميل بواسطة بوت أبو كيان")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, "user_photo.jpg")
    await message.answer("اختر فلتر الأيفون المناسب:", reply_markup=get_photo_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
