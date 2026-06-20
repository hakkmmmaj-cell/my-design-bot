import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ضع التوكن الجديد هنا
TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# أمر البدء
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("أهلاً بك يا أبو كيان، البوت يعمل الآن!")

# الرد على أي رسالة
@dp.message()
async def echo(message: types.Message):
    await message.answer("أهلاً بك يا أبو كيان")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
