from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from PIL import Image, ImageEnhance, ImageFilter
import io
import asyncio

# ضع التوكن الخاص بك هنا
TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً! أرسل لي صورة، ثم اكتب أي أمر مثل: 'دقة عالية' أو 'فلتر أبيض وأسود'.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    # تحميل الصورة
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, "input.jpg")
    
    img = Image.open("input.jpg")
    
    # معالجة بسيطة (مثلاً زيادة التباين كنوع من تحسين الدقة)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    img.save("output.jpg")
    await message.answer_photo(photo=types.FSInputFile("output.jpg"), caption="تم تحسين الصورة.")

@dp.message(F.text)
async def apply_filter(message: types.Message):
    if "أبيض وأسود" in message.text:
        img = Image.open("input.jpg").convert("L")
        img.save("filtered.jpg")
        await message.answer_photo(photo=types.FSInputFile("filtered.jpg"))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
