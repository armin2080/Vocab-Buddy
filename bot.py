from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from typing import Final
from database import DatabaseManager


# Load the bot token from the config file
with open("config.json", "r") as f:
    config = json.load(f)
TOKEN: Final = config["BOT_TOKEN"]


# Start database manager
db_manager = DatabaseManager()









async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    username = update.effective_user.username
    user_exists = db_manager.fetch_all('users', where_clause='telegram_id', where_args=[user_id])
    if not user_exists:
        db_manager.add_instance('users', columns=['telegram_id', 'username'], new_vals=[user_id, username])
        text = f"Hello @{username}! \nWelcome to Vocab Buddy! You have been registered."
    else:
        text = f"Hello @{username}! \nWelcome back to Vocab Buddy!"

    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()