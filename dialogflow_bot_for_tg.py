import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dotenv import load_dotenv
from df_manager import get_df_response


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Здравствуйте!",
    )


def respond(update: Update, context: CallbackContext) -> None:
    df_response, is_fallback = get_df_response(os.environ["PROJECT_ID"], update.message.chat_id, update.message.text)
    update.message.reply_text(df_response)


if __name__ == "__main__":
    load_dotenv(".env")
    updater = Updater(os.environ["TG_TOKEN"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))
    updater.start_polling()
    updater.idle()
