import os
import time
import subprocess
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

# We load the bot token from the .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize user id variable
user_id = ""

# Function to handle the /start command -> Starts running the ping_collector
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_id 
    user_id = update.effective_chat.id

    if os.path.isdir(f'data/{user_id}') == True:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are already registered")
    else:
        os.mkdir(f'data/{user_id}/')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You have been registered in our database")
        await InlineKeyboardButton('asd', callback_data='asdsss')
    
    

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register the command handlers
    application.add_handler(CommandHandler("start", start_command))

    # Start the bot   
    application.run_polling()

if __name__ == '__main__':
    main()