import glob
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from utils import *

logging.basicConfig(filename='bot.log', level=logging.INFO)
TOKEN = credentials.TOKEN


def greet_user(update, context):
    # update это нам передаст диспетчер там будет инфа, которую нам передал телеграм
    # context это непонятное что-то..
    print('вызван start')
    smile = credentials.USER_EMOJI[0]
    smile = emojize(smile, use_aliases=True)
    update.message.reply_text(f'Привет, попроси меня показать тебе котика {smile}', reply_markup=main_keyboard())


def play_random_number(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if bot_number > user_number:
        message = f'Вы ввели {user_number}, у бота {bot_number}. Вы проиграли!'
    elif bot_number == user_number:
        message = f'Вы ввели {user_number}, у бота {bot_number}. Ничья!'
    else:
        message = f'Вы ввели {user_number}, у бота {bot_number}. Вы победили!'
    return message


def send_photo(update, context, meaning='cat'):
    counter = get_user_counter(context.user_data)
    if counter < 0:
        message = f'Вы слишком часто просите показать котиков {counter}\nПохоже у вас котозависимость.'
        send_text(update, context, message)
    else:
        mask = credentials.FILE_MASKS[meaning]
        photos_list = glob.glob(f'images/{mask}')
        photo = choice(photos_list)
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=open(photo, 'rb'), reply_markup=main_keyboard())


def send_text(update, context, message):
    update.message.reply_text(message)


def echo_text(update, context):
    message = update.message.text
    chat_id = update.effective_chat.id
    print(chat_id, message)
    meaning = find_the_meaning(message)

    if meaning == 'smile':
        update.message.reply_text(f'{choice(["Mяу-Мяу", "Мурррр"])} {get_smile()}')

    elif meaning == 'arrrgh':
        update.message.reply_text(f'{choice(["Фррр", "Кусь тебя!", "Цап-царап!"])} {get_smile(":smirk_cat:")}')

    elif meaning == 'weather':
        update.message.reply_text(get_weather())

    elif meaning == 'exchange':
        update.message.reply_text(get_exchange())

    else:
        send_photo(update, context, meaning=meaning)


def user_location(update, context):
    coords = update.message.location
    print(coords)


def main():
    my_bot = Updater(token=TOKEN, use_context=True)
    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_photo))
    dp.add_handler(MessageHandler(Filters.location, user_location))
    dp.add_handler(MessageHandler(Filters.text, echo_text))

    logging.info('бот стартовал')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()