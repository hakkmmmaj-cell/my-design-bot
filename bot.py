import asyncio
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
from PIL import Image, ImageEnhance, ImageDraw

# 1. إعدادات البوت (ضع التوكن الخاص بك هنا)
TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 2. دالة "التصميم والختم" الاحترافية
def process_image(input_path, output_path):
    img = Image.open(input_path)
    
    # تحسين الصورة (تصميم)
    img = ImageEnhance.Contrast(img).enhance(1.4) # زيادة التباين
    img = ImageEnhance.Sharpness(img).enhance(1.8) # زيادة الحدة
    
    # إضافة الحقوق (الختم)
    draw = ImageDraw.Draw(img)
    text = "بوت أبو كيان"
    # وضع النص في أسفل يمين الصورة
    width, height = img.size
    draw.text((width - 150, height - 40), text, fill=(255, 255, 255)) 
    
    img.save(output_path)

# 3. معالجة التحميل من تيك توك
@dp.message(F.text.contains("tiktok.com"))
async def handle_tiktok(message: types.Message):
    await message.answer("📥 جاري التحميل، لحظات...")
    ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        await message.answer_video(video=FSInputFile("video.mp4"), caption="تم التحميل من بوت أبو كيان ✨")
    except:
        await message.answer("خطأ في التحميل، جرب رابطاً آخر.")

# 4. معالجة الصور (التصميم + الختم)
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("🎨 جاري التصميم ووضع الحقوق...")
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, "input.jpg")
    
    process_image("input.jpg", "output.jpg")
    await message.answer_photo(photo=FSInputFile("output.jpg"), caption="تصميم احترافي بلمسة أبو كيان ✨")

# 5. تشغيل البوت
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
