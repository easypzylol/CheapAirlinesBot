 import telebot
from flask import Flask, request
import os

BOT_TOKEN = "8478581885:AAGzE9c196b9ryrx3GMSlFuAyZeSdg4-8rw"
WEBHOOK_URL = "https://cheapairlinesbot.onrender.com/"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Handle /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    first_name = message.from_user.first_name or "there"
    bot.send_message(message.chat.id, f"👋 Welcome, {first_name}!\n\n🔗 Check our channel for updates:\nhttps://t.me/senseiRedirect")

# Webhook route
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Home route (just for confirmation)
@app.route("/", methods=['GET'])
def index():
    return "Bot is live!", 200

# Set webhook and run server
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + BOT_TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))