import credentials
from emoji import emojize
import glob
import logging
from pprint import pprint

from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)
TOKEN = credentials.TOKEN

CATS_DICT = ['кота', 'котика', 'котейку', 'кошака']


def get_smile(txt = ':kissing_heart:'):
    smile = emojize(txt, use_aliases=True)
    return smile


def get_random_smile():
    smile = choice(credentials.USER_EMOJI)
    smile = emojize(smile, use_aliases=True)
    return smile


def greet_user(update, context):
    # update это нам передаст диспетчер там будет инфа, которую нам передал телеграм
    # context это непонятное что-то..
    print('вызван start')
    smile = credentials.USER_EMOJI[0]
    smile = emojize(smile, use_aliases=True)
    update.message.reply_text(f'Привет, попроси меня показать тебе {choice(CATS_DICT)}! {smile}')


def play_random_number(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if bot_number > user_number:
        message = f'Вы ввели {user_number}, у бота {bot_number}. Вы проиграли!'
    elif bot_number == user_number:
        message = f'Вы ввели {user_number}, у бота {bot_number}. Ничья!'
    else:
        message = f'Вы ввели {user_number}, у бота {bot_number}. Вы победили!'
    return message


def guess_number(update, context):
    print('вызван guess')
    if context.args:

        try:
            user_number = int(context.args[0])
            message = play_random_number(user_number)

        except (TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите число'

    update.message.reply_text(message)


def echo_text(update, context):

    message = update.message.text
    chat_id = update.effective_chat.id
    print(chat_id, message)

    for cat in CATS_DICT:
        if cat in message:
            send_cat(update, context)
            return

    for compliment in credentials.COMPLIMENTS:
        if compliment in message.lower():
            update.message.reply_text(f'Мяy-мяy {get_smile()}')
            return

    for insult in credentials.INSULTS:
        if insult in message.lower():
            update.message.reply_text(f'Фррр {get_smile(":smirk_cat:")}')
            return


def send_cat(update, context):
    print('cats')
    cat_photos_list = glob.glob('images/*')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def main():
    my_bot = Updater(token=TOKEN, use_context=True)
    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_cat))
    dp.add_handler(MessageHandler(Filters.text, echo_text))

    logging.info('бот стартовал')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()



