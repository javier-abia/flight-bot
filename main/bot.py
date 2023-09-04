import os
import time
import subprocess
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, ApplicationBuilder, filters, Application

# We load the bot token from the .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize user id variable
user_id = ""

# Dictionary to keep track of whether a user has been welcomed
welcomed_users = {}


# Function to handle the /start command -> Starts running the flight bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_id 
    user_id = update.effective_chat.id

    if os.path.isdir(f'data/{user_id}') == True:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are already registered")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Remember that you can use the menu by clicking in the left down corner or by typing /menu")

    else:
        os.mkdir(f'data/{user_id}/')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to your Flight Assistant Bot! To start, let me ask you some questions")

        

# Function to handle the /menu
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        button_flights = InlineKeyboardButton('Check new flights', callback_data='new_flights')
        button_config = InlineKeyboardButton('Configuration', callback_data='config')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_flights],[button_config]])
        await context.bot.send_message(chat_id=update.effective_chat.id, text="What do you want to do?", reply_markup=keyboard)


# Function to handle the callback query
async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "config":
        button_departures = InlineKeyboardButton('Change departures', callback_data='change_departures')
        button_price = InlineKeyboardButton('Change price', callback_data='change_price')
        button_frequency = InlineKeyboardButton('Change frequency', callback_data='change_frequency')
        button_back = InlineKeyboardButton('Back', callback_data='menu')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_departures],[button_price],[button_frequency],[button_back]])

        await context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id=query.message.message_id, reply_markup=keyboard)
        await context.bot.answer_callback_query(query.id)

    if data == "change_price":
        # Send a message
        await context.bot.send_message(chat_id=update.effective_chat.id, text="The price has been changed.")
        await context.bot.answer_callback_query(query.id)


    if data == "menu":
        # Get the keyboard from the menu_command function
        keyboard = await menu_command(update, context)

        # Send the keyboard to the user
        await context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id=query.message.message_id, reply_markup=keyboard)
        

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register the command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", menu_command))

    application.add_handler(CallbackQueryHandler(callback_query_handler))


    # Start the bot   
    application.run_polling()

if __name__ == '__main__':
    main()
