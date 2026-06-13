import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

unread_messages = {}

def start(update, context):
    update.message.reply_text("Hello! I’ll track unread messages for you.")

def handle_message(update, context):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in unread_messages:
        unread_messages[user_id] = []
    unread_messages[user_id].append(text)

    update.message.reply_text("Got your message! Marked as unread.")

def show_unread(update, context):
    user_id = update.message.from_user.id
    if user_id in unread_messages and unread_messages[user_id]:
        msgs = "\n".join(unread_messages[user_id])
        update.message.reply_text(f"Your unread messages:\n{msgs}")
        unread_messages[user_id] = []
    else:
        update.message.reply_text("No unread messages!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("unread", show_unread))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
