import random

import credentials
from emoji import emojize
import glob
import logging
import pymorphy2
from pprint import pprint
import re
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests
from lxml import etree

logging.basicConfig(filename='bot.log', level=logging.INFO)
TOKEN = credentials.TOKEN


def get_exchange(valute='Доллар США'):
    url = credentials.EXCHANGE_URL
    response = requests.get(url)
    root = etree.fromstring(response.content)
    for elem in root.getchildren():
        if elem[3].text == valute:
            current_course = float(elem[4].text.replace(',', '.'))
            break
    return current_course


def get_weather(city_name='Moscow,Russia'):
    url = credentials.WEATER_URL
    params = {
        'key': credentials.WEATHER_API_KEY,
        'q': city_name,
        'format': 'json',
        'num_of_days': 1,
        'lang': 'ru',
    }

    response = requests.get(url, params)
    # print(f'wheather status code {response.status_code}')
    weather = response.json()
    pprint(weather)
    if 'data' in weather:
        if 'current_condition' in weather['data']:
            try:
                current_weather = weather['data']['current_condition'][0]
                weather_list = [
                    f'Температура: {current_weather["temp_C"]}, ощущается как {current_weather["FeelsLikeC"]}',
                    f'Влажность {current_weather["humidity"]}, {current_weather["lang_ru"][0]["value"]}',
                    f'Cкорость ветра {current_weather["windspeedKmph"]} км/ч']
                return '\n'.join(weather_list)
            except (IndexError, TypeError):
                print('Weather mistake!')
                return 'При определении погоды возникли ошибки'
    else:
        return 'Сервис погоды временно недоступен'


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


def normalized(message):
    print(f'функция normalized на вход пришло: {message}')
    regexp = r'\w+'
    regexp_compiled = re.compile(regexp)
    morph = pymorphy2.MorphAnalyzer()

    message_lower = message.lower()
    message_by_words = regexp_compiled.findall(message_lower)
    message_normalized = []
    for word in message_by_words:
        message_normalized.append(morph.normal_forms(word)[0])
    print(f'на выходе получили {message_normalized}')
    return message_normalized


def is_it_intersect(s1, s2):
    s3 = list(set(s1).intersection(set(s2)))
    print(f'is_it_intersect {s3, len(s3)}')
    return len(s3) > 0


def find_the_meaning(message):

    norm_message = normalized(message)
    meaning = ''

    if is_it_intersect(credentials.NAMES, norm_message):
        meaning = 'names'

    elif is_it_intersect(['погода', 'погодка'], norm_message):
        meaning = 'weather'

    elif ('курс' in norm_message) and (is_it_intersect(['доллар', 'бакс'], norm_message)):
        meaning = 'exchange'

    elif ('не' in norm_message) and ('показывать' in norm_message) and (is_it_intersect(credentials.CATS_DICT, norm_message)):
        print('meaning is : котейка плачет')
        meaning = 'sad_cat'

    elif ('показать' in norm_message) and \
            (('кот' in norm_message) or ('кошка' in norm_message) or ('котик' in norm_message)):
        meaning = 'cat'

    elif len(list(set(credentials.CATS_DICT).intersection(set(norm_message)))):
        meaning = 'cat'

    # elif len(list(set(credentials.COMPLIMENTS).intersection(set(norm_message)))):
    elif is_it_intersect(credentials.COMPLIMENTS, norm_message):
        meaning = 'smile'

    elif len(list(set(credentials.INSULTS).intersection(set(norm_message)))):
        meaning = 'arrrgh'

    elif ('показать' in norm_message) and ('сушка' in norm_message):
        meaning = 'sushka'

    elif ('показать' in norm_message) and \
            (('собака' in norm_message) or ('сметанка' in norm_message)):
        meaning = 'dog'

    elif 'сметана' in norm_message:
        meaning = 'cream'

    elif ('ромка' in norm_message) and ('настоящий' in norm_message):
        meaning = 'real_rom'

    elif 'ромка' in norm_message:
        meaning = 'bearded'
    print(f'meaning {meaning}')
    return meaning


def get_user_counter(update, context):
    user_data = context.user_data
    if 'counter' not in user_data:
        user_data['counter'] = 1
    elif user_data['counter'] > 3:
        user_data['counter'] = -3
    else:
        user_data['counter'] += 1

    # print(f'User counter {user_data["counter"]}')
    print(user_data)
    return user_data['counter']


def send_photo(update, context, meaning='cat'):
    counter = get_user_counter(update, context)
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
        update.message.reply_text(f'{random.choice(["Mяу-Мяу", "Мурррр"])} {get_smile()}')

    elif meaning == 'arrrgh':
        update.message.reply_text(f'{random.choice(["Фррр", "Кусь тебя!", "Цап-царап!"])} {get_smile(":smirk_cat:")}')

    elif meaning == 'weather':
        update.message.reply_text(get_weather())

    elif meaning == 'exchange':
        update.message.reply_text(get_exchange())

    else:
        send_photo(update, context, meaning=meaning)


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Покажи котика', 'Покажи сметанку'],
        ['Курс доллара', 'Что с погодой'],
    ])


def main():
    my_bot = Updater(token=TOKEN, use_context=True)
    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('cat', send_photo))
    dp.add_handler(MessageHandler(Filters.text, echo_text))

    logging.info('бот стартовал')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()