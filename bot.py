import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import yt_dlp
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, vfx

TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"
MY_NAME = "『أبـو كـيـان』"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# دالة التحميل
def download_tiktok(url):
    ydl_opts = {'outtmpl': 'video.mp4', 'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "video.mp4"

# دالة التصميم (الفلاتر والاسم)
def add_design(video_path):
    output = "final.mp4"
    clip = VideoFileClip(video_path)
    # إضافة الفلتر (زيادة التباين والحدة)
    clip = clip.fx(vfx.colorx, 1.2).fx(vfx.lum_contrast, 0, 10, 1.1)
    
    txt_clip = TextClip(MY_NAME, fontsize=40, color='yellow', font='Arial')
    txt_clip = txt_clip.set_duration(clip.duration).set_position(("center", "bottom"))
    
    video = CompositeVideoClip([clip, txt_clip])
    video.write_videofile(output, codec="libx264", audio_codec="aac", bitrate="8000k")
    return output

# الترحيب
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"أهلاً بك! {MY_NAME} يرحب بك في بوت التصميم والتحميل.\n\nأرسل رابط تيك توك وسأقوم بتصميمه لك!")

# المعالجة
@dp.message(F.text.contains("tiktok.com"))
async def handle_tiktok(message: types.Message):
    status_msg = await message.answer("جاري جلب الفيديو وتطبيق فلتر الآيفون... انتظر.")
    try:
        raw_video = download_tiktok(message.text)
        final_video = add_design(raw_video)
        await message.answer_video(types.FSInputFile(final_video))
        os.remove(raw_video)
        os.remove(final_video)
        await status_msg.delete()
    except Exception as e:
        await message.answer(f"حدث خطأ: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
