from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import secrets

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hey {update.effective_user.first_name}! quiereme')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Soy un boooot, hablame!"
    )


app = ApplicationBuilder().token(secrets.telegram_bot_token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler('start', start))

app.run_polling()
