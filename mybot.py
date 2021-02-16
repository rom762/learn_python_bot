import credentials
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pprint import pprint
import logging
logging.basicConfig(filename='bot.log', level=logging.INFO)

TOKEN = credentials.TOKEN


def greet_user(update, context):
    # update это нам передаст диспетчер там будет инфа, которую нам передал телеграм
    # context это непонятное что-то..
    print('вызван start')
    print(1/0)
    update.message.reply_text('Привет, пользователь!')
    pprint(update)


def guess_number(update, context):
    print('вызван guess')
    pass


def echo_text(update, config):

    message = update.message.text
    print(message)
    update.message.reply_text(message)


def main():
    my_bot = Updater(token=TOKEN, use_context=True)
    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(MessageHandler(Filters.text, echo_text))


    logging.info('бот стартовал')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()



