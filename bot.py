from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# دالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط الفيديو وسأعطيك خيارات الجودة!")

# معالجة الرابط وعرض الأزرار
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    # حفظ الرابط في السياق لاستخدامه لاحقاً
    context.user_data['url'] = url
    
    # الحصول على معلومات الفيديو
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        
    keyboard = [
        [InlineKeyboardButton("1080p", callback_data='1080')],
        [InlineKeyboardButton("720p", callback_data='720')],
        [InlineKeyboardButton("360p", callback_data='360')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر الجودة المطلوبة:", reply_markup=reply_markup)

# دالة التحميل بعد اختيار الجودة
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    quality = query.data
    url = context.user_data.get('url')

    await query.edit_message_text(f"جاري تحميل الفيديو بجودة {quality}p... انتظر قليلاً")

    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
        'outtmpl': 'video.mp4',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    await query.message.reply_video(video=open('video.mp4', 'rb'))

# إعداد البوت
app = ApplicationBuilder().token("8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(button_callback))

app.run_polling()
