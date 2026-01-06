import os
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

# ================== НАСТРОЙКИ ==================

BOT_TOKEN = os.getenv("BOT_TOKEN")
MS_API_KEY = os.getenv("MS_API_KEY")

if not BOT_TOKEN or not MS_API_KEY:
    raise RuntimeError("Не заданы BOT_TOKEN или MS_API_KEY")

# ================== DEEPSEEK ==================

client = OpenAI(
    base_url="https://api-inference.modelscope.ai/v1",
    api_key=MS_API_KEY,
)

def ask_deepseek(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2",
            messages=[
                {"role": "user", "content": text}
            ],
            extra_body={
                "enable_thinking": False
            }
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка DeepSeek: {e}"

# ================== TELEGRAM ==================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    answer = ask_deepseek(user_text)
    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    print("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
