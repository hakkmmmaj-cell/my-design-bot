import asyncio
import sqlite3
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageEnhance, ImageFilter
import yt_dlp

TOKEN = '8835938014:AAEE7yIeXt7K3EkUUmxUyl4vAtO_LkTwJn8' # ضع التوكن الخاص بك هنا
bot = Bot(token=TOKEN)
dp = Dispatcher()

# قاعدة البيانات
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)')
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()
    return [u[0] for u in users]

# الأوامر
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    add_user(message.from_user.id)
    await message.answer(f"أهلاً بك {message.from_user.first_name}!\nأبو كيان يرحب بك في بوت الخدمات.")

@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):
    MY_ID = 6705284698‪  # <--- ضع رقمك الشخصي هنا
    if message.from_user.id != MY_ID:
        return
    msg_text = message.text.replace("/broadcast ", "")
    for user_id in get_all_users():
        try: await bot.send_message(user_id, msg_text)
        except: pass
    await message.answer("تمت الإذاعة!")

# الفلاتر والتحميل (نفس الكود السابق...)
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f"img_{message.from_user.id}.jpg")
    await message.answer("تم حفظ الصورة، اختر الفلتر.")

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
