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

    welcome_text = (
        f"👋 Welcome, {message.from_user.first_name}!\n\n"
        "Thanks for starting the bot.\n\n"
        "🔗 Check out our channel for latest updates:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

print("🤖 Bot is running...")
bot.polling()