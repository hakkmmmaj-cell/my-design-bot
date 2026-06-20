from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

# التوكن الخاص بك
TOKEN = '8656297195:AAHCaNApCb0oi6lElpvxamf3uL8-L9DaRec'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# أمر البدء (Start)
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "مرحباً! كيف يمكن أن أساعدك اليوم؟\n\n"
        "━━━━━━━━━━━━\n"
        "هذا البوت خاص بـ أبو كيان © 2026"
    )

# الرد على الرسائل الأخرى
@dp.message()
async def echo(message: types.Message):
    response = f"أهلاً بك، أنا هنا للمساعدة.\n\n━━━━━━━━━━━━\nبوت خاص بـ أبو كيان"
    await message.answer(response)

async def main():
    print("البوت يعمل الآن...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
