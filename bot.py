import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔴 مفاتيحك
BOT_TOKEN = "8835938014:AAE68WNbEemZHQYK_5Z810M5uqrONkrmBYc"
OPENROUTER_API_KEY = "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"


# 🤖 دالة الذكاء الاصطناعي
def ask_ai(text):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [{"role": "user", "content": text}]
            },
            timeout=30
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("AI ERROR:", e)
        return "⚠️ صار خطأ بالذكاء الاصطناعي"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بيك\nأرسل أي سؤال وأنا أجاوبك 🤖"
    )


# 💬 الدردشة
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    reply = ask_ai(user_text)
    await update.message.reply_text(reply)


# ▶️ تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
