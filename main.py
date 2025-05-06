import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def format_prompt(user_message):
    return (
        "You are Tanjiro Kamado from Demon Slayer. Respond kindly, respectfully, and with empathy. "
        f"Here is the message: {user_message}"
    )

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    prompt = format_prompt(user_text)

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, json=payload, headers=headers)

    if response.status_code == 200:
        try:
            reply_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            reply_text = "Sorry, I couldn't understand the response."
    else:
        reply_text = "Sorry, something went wrong while talking to the AI."

    await update.message.reply_text(reply_text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), respond))
    print("Bot is running...")
    app.run_polling()
