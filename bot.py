import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

unread_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I’ll track unread messages for you.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in unread_messages:
        unread_messages[user_id] = []
    unread_messages[user_id].append(text)

    await update.message.reply_text("Got your message! Marked as unread.")

async def show_unread(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in unread_messages and unread_messages[user_id]:
        msgs = "\n".join(unread_messages[user_id])
        await update.message.reply_text(f"Your unread messages:\n{msgs}")
        unread_messages[user_id] = []
    else:
        await update.message.reply_text("No unread messages!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("unread", show_unread))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
