import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import greet_user, guess_number, user_location, echo_text, send_text, send_photo
import credentials


logging.basicConfig(filename='bot.log', level=logging.INFO)
TOKEN = credentials.TOKEN


def main():
    my_bot = Updater(token=TOKEN, use_context=True)
    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_photo))
    dp.add_handler(MessageHandler(Filters.location, user_location))
    dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_handler(MessageHandler(Filters.text, send_text))

    logging.info('бот стартовал')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()