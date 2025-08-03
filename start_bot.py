import telebot
from telebot import types
from flask import Flask, request

# === CONFIG ===
BOT_TOKEN = "8478581885:AAGzE9c196b9ryrx3GMSlFuAyZeSdg4-8rw"
WEBHOOK_URL = "https://cheapairlinesbot.onrender.com"  # Replace with your Render URL
CHANNEL_LINK = "https://t.me/senseiRedirect"
LOG_FILE = "users.txt"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# === FUNCTION: Log user ID + username ===
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

# === COMMAND: /start ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    log_user(user_id, username)

    markup = types.InlineKeyboardMarkup()
    join_btn = types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)
    markup.add(join_btn)

    welcome_text = (
        "🎉 *Welcome to our Travel Deals Bot, Sensei Reloaded* 🔥!\n\n"
        "✈️ *Get ready for amazing travel deals and exclusive offers!*\n\n"
        "📢 *Join our channel for the latest updates:*\n"
        f"{CHANNEL_LINK}\n\n"
        "🌍 *We'll notify you about:*\n"
        "• Flight deals and discounts\n"
        "• Hotel offers\n"
        "• Travel packages\n"
        "• Last-minute deals\n\n"
        "Start your journey with us! 🧳"
    )

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )

# === WEBHOOK HANDLER ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return {"ok": True}

# === HOME ROUTE ===
@app.route("/", methods=["GET"])
def index():
    return "Bot is live ✅"

# === SET WEBHOOK ===
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=10000)