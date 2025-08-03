import telebot
from telebot import types

BOT_TOKEN = "8478581885:AAGzE9c196b9ryrx3GMSlFuAyZeSdg4-8rw"
CHANNEL_LINK = "https://t.me/senseiRedirect"
LOG_FILE = "users.txt"

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
        f"👋 Welcome, {message.from_user.first_name}!
"
        "Thanks for starting the bot.

"
        "🔗 Check out our channel for latest updates:",
        reply_markup=markup)

print("🤖 Bot is running...")
bot.polling()