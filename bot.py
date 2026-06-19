import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

# ضع التوكن والمفتاح هنا مباشرة
TELEGRAM_TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'
API_KEY = 'Sk-CwB3oqCojMmSvPaBQI4GW4vOT4w7NZmShvk6UDMbAalcUDXr'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message):
    await message.answer("تم تفعيل البوت بالمفاتيح المباشرة!")

@dp.message()
async def chat(message):
    await message.answer("البوت يعمل، لكن يحتاج لربط مكتبة الصور ليعمل التصميم.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
