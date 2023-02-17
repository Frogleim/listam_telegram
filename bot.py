import logging
import telegram
from telegram import ReplyKeyboardMarkup, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import time
import threading
import pandas as pd
import get_data
import config


class Bots:
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.updater = Updater(config.TOKEN)

    @staticmethod
    def start(update, context):
        """Send a message when the command /start is issued."""

        update.message.reply_text(
            'Hi! This is List.am bot! '
            'I will deliver new states offer every 24 hours.\n\n'
            'Please wait, until I try to get new data for you\n'
            'it can take a couple minutes',
        )
        res = get_data.run()
        print(res)
        try:
            for result in res:
                update.message.reply_text(
                    f'Name: {result["name"]}'
                    f'Price: {result["price"]}'
                    f'URL: {result["url"]}',

                )
        except Exception as e:
            update.message.reply_text(
                'Unfortunately, there is no new offer today'
            )
            print(e)

    @staticmethod
    def cancel(update, _):
        update.message.reply_text(
            'You subscription was canceled'
        )
        return ConversationHandler.END

    def error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

    def run(self):
        """Start the bot."""
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_error_handler(self.error)

        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    my_bot = Bots()
    my_bot.run()
