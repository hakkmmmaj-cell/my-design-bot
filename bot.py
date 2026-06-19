import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

# التوكن والمفتاح الخاص بك
TELEGRAM_TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'
STABILITY_KEY = 'Sk-CwB3oqCojMmSvPaBQI4GW4vOT4w7NZmShvk6UDMbAalcUDXr'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("أهلاً بك! أرسل وصفاً لأي صورة وسأقوم بتصميمها لك.")

@dp.message()
async def generate(message: types.Message):
    await message.answer("جاري تصميم الصورة، يرجى الانتظار...")
    
    # الطلب إلى Stability AI
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={"authorization": f"Bearer {STABILITY_KEY}", "accept": "image/*"},
        files={"none": ""},
        data={"prompt": message.text, "output_format": "jpeg"}
    )
    
    if response.status_code == 200:
        await message.answer_photo(photo=types.BufferedInputFile(response.content, filename="image.jpg"))
    else:
        await message.answer(f"خطأ {response.status_code}: لا يمكن الاتصال بالخدمة. تأكد من رصيد المفتاح.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
