import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ضع التوكن الجديد الخاص بك هنا
TOKEN = '8835938014:AAFBTNbOwxzPbpFtR6kWoVTcU2ofRbWke70'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# الترحيب مع إضافة حقوق أبو كيان
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Abu Kayan bot welcomes you! How can I help you today?\n\n"
        "--------------------------\n"
        "Developer: Abu Kayan © 2026"
    )

# الرد على أي رسالة مع إضافة الحقوق
@dp.message()
async def echo_handler(message: types.Message):
    response = f"You said: {message.text}\n\n--------------------------\nPowered by Abu Kayan"
    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
