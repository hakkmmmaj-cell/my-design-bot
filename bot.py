import json, os, time
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# 🔴 التوكن
BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

# 🔵 القناة
CHANNEL_USERNAME = "@A_1_1_1W"
CHANNEL_LINK = "https://t.me/A_1_1_1W"

# 👑 الأدمن
ADMIN_ID = 123456789

# 💾 قاعدة بيانات بسيطة
DB_FILE = "db.json"

if os.path.exists(DB_FILE):
    db = json.load(open(DB_FILE))
else:
    db = {"users": [], "banned": [], "downloads": 0}

def save():
    json.dump(db, open(DB_FILE, "w"))

# 🧠 وضع المستخدم
user_mode = {}
last_time = {}

# =====================
# فحص اشتراك
# =====================
async def check_sub(user_id, bot):
    try:
        m = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return m.status in ["member", "administrator", "creator"]
    except:
        return False

# =====================
# منع سبام
# =====================
def anti_spam(user_id):
    now = time.time()
    if user_id in last_time and now - last_time[user_id] < 3:
        return False
    last_time[user_id] = now
    return True

# =====================
# تحميل فيديو
# =====================
def download_video(url):
    yt_dlp.YoutubeDL({"format": "best", "outtmpl": "video.mp4"}).download([url])

# =====================
# تحميل صوت
# =====================
def download_audio(url):
    yt_dlp.YoutubeDL({
        "format": "bestaudio",
        "outtmpl": "audio.mp3",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3"
        }]
    }).download([url])

# =====================
# أزرار
# =====================
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 فيديو", callback_data="video")],
        [InlineKeyboardButton("🎵 صوت", callback_data="audio")],
        [InlineKeyboardButton("📊 إحصائيات", callback_data="stats")],
        [InlineKeyboardButton("📢 القناة", url=CHANNEL_LINK)]
    ])

# =====================
# /start
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user

    if u.id not in db["users"]:
        db["users"].append(u.id)
        save()

    if u.id in db["banned"]:
        await update.message.reply_text("🚫 أنت محظور")
        return

    if not await check_sub(u.id, context.bot):
        await update.message.reply_text(
            "👑 اشترك بالقناة أولاً",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("اشتراك", url=CHANNEL_LINK)]])
        )
        return

    await update.message.reply_text("👑 أهلاً بك في أقوى بوت بالعالم 🔥", reply_markup=menu())

# =====================
# أزرار
# =====================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    if uid in db["banned"]:
        return

    if q.data == "video":
        user_mode[uid] = "video"
        await q.edit_message_text("📥 أرسل الرابط")

    elif q.data == "audio":
        user_mode[uid] = "audio"
        await q.edit_message_text("🎵 أرسل الرابط")

    elif q.data == "stats":
        if uid != ADMIN_ID:
            await q.edit_message_text("❌ للأدمن فقط")
            return

        await q.edit_message_text(
            f"👑 Ultra Stats:\n\n"
            f"👥 Users: {len(db['users'])}\n"
            f"📥 Downloads: {db['downloads']}\n"
            f"🚫 Banned: {len(db['banned'])}"
        )

# =====================
# رسائل
# =====================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    text = update.message.text

    if u.id in db["banned"]:
        return

    if not anti_spam(u.id):
        return

    if "http" not in text:
        await update.message.reply_text("📌 أرسل رابط فقط")
        return

    mode = user_mode.get(u.id, "video")

    await update.message.reply_text("⚡ جاري المعالجة...")

    try:
        if mode == "audio":
            download_audio(text)
            with open("audio.mp3", "rb") as f:
                await update.message.reply_audio(f)
        else:
            download_video(text)
            with open("video.mp4", "rb") as f:
                await update.message.reply_video(f)

        db["downloads"] += 1
        save()

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ فشل التحميل")

# =====================
# تشغيل
# =====================
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
