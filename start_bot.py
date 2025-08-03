import telebot
from telebot import types

BOT_TOKEN = "8478581885:AAGzE9c196b9ryrx3GMSlFuAyZeSdg4-8rw"
CHANNEL_LINK = "https://t.me/senseiRedirect"
LOG_FILE = "users.txt"
WEBHOOK_URL = "https://your-render-url.onrender.com/"  # Replace this with your actual Render domain

bot = telebot.TeleBot(BOT_TOKEN)

def log_user(user_id, username):
    try:
        with open(LOG_FILE, "r") as f:
            users = f.read().splitlines()
    except FileNotFoundError:
        users = []

    entry = f"{user_id} - {username}"
    if entry not in users:
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    log_user(user_id, username)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    bot.send_message(message.chat.id,
        f"👋 Welcome, {message.from_user.first_name}!\n"
        "Thanks for starting the bot.\n\n"
        "🔗 Check out our channel for latest updates:",
        reply_markup=markup)

import flask

app = flask.Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    json_str = flask.request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=["GET"])
def root():
    return "Bot is alive!", 200

if __name__ == "__main__":
    import os
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + BOT_TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))