import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageEnhance, ImageFilter
import yt_dlp

# ضع توكنك هنا
TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. الترحيب الخاص بك
@dp.message(Command("start"))
async def welcome(message: types.Message):
    await message.answer(f"أهلاً بك يا {message.from_user.first_name}!\n\n**أبو كيان يرحب بك** في بوت الخدمات الشامل.\n\nأرسل رابط تيك توك للتحميل، أو صورة لتطبيق فلاتر الأيفون الاحترافية. ✨")

# 2. قائمة الفلاتر
def get_photo_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 فلتر الأيفون الاحترافي", callback_data="iphone")],
        [InlineKeyboardButton(text="✨ إضاءة سينمائية", callback_data="bright")],
        [InlineKeyboardButton(text="💎 حدة 4K خارقة", callback_data="hd")]
    ])

# 3. المعالجة الاحترافية (مع عزل المستخدمين)
@dp.callback_query(F.data.in_({"iphone", "bright", "hd"}))
async def apply_filter(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    input_path = f"img_{user_id}.jpg"
    output_path = f"out_{user_id}.jpg"
    
    if not os.path.exists(input_path):
        await callback.answer("يرجى إرسال الصورة أولاً!")
        return

    await callback.answer("جاري المعالجة..")
    try:
        img = Image.open(input_path)
        if callback.data == "iphone":
            img = ImageEnhance.Contrast(img).enhance(1.2)
            img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
        elif callback.data == "bright":
            img = ImageEnhance.Brightness(img).enhance(1.3)
        elif callback.data == "hd":
            img = img.filter(ImageFilter.DETAIL).filter(ImageFilter.SHARPEN)

        img.save(output_path)
        await callback.message.answer_photo(photo=types.FSInputFile(output_path), caption="تمت المعالجة بواسطة بوت أبو كيان ✨")
    except Exception:
        await callback.message.answer("حدث خطأ، حاول مجدداً.")

# 4. تحميل تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def download_tiktok(message: types.Message):
    status = await message.answer("🔄 جاري التحميل..")
    try:
        ydl_opts = {'outtmpl': f'vid_{message.from_user.id}.mp4', 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        await message.answer_video(video=types.FSInputFile(f'vid_{message.from_user.id}.mp4'), caption="تم التحميل بواسطة بوت أبو كيان 🚀")
        await bot.delete_message(chat_id=message.chat.id, message_id=status.message_id)
    except Exception:
        await message.answer("فشل التحميل، تأكد من الرابط.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f"img_{message.from_user.id}.jpg")
    await message.answer("تم حفظ الصورة، اختر الفلتر:", reply_markup=get_photo_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
