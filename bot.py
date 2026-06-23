import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔴 التوكن
BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"

# 🔵 مفتاح Gemini
GEMINI_API_KEY = "AQ.Ab8RN6KwcS-c-biVhi3x_d_fCcnxOWYNMLmyPhMzTQQm4OHM4w"

# إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بيك\nأرسل أي رسالة وأنا أجاوبك 🤖"
    )


# 💬 الدردشة
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = model.generate_content(user_text)

        # حماية من الرد الفارغ
        if not response or not hasattr(response, "text"):
            await update.message.reply_text("⚠️ ما كدرت أجيب رد، حاول مرة ثانية")
            return

        await update.message.reply_text(response.text)

    except Exception as e:
        print("GEMINI ERROR:", e)
        await update.message.reply_text("⚠️ صار خطأ بالذكاء الاصطناعي")


# تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
