import re
import time
from pprint import pprint

import pymorphy2
import requests
from emoji import emojize
from random import choice, randint
from lxml import etree
from telegram import ReplyKeyboardMarkup, KeyboardButton
import credentials


def is_it_intersect(s1, s2):
    s3 = list(set(s1).intersection(set(s2)))
    print(f'is_it_intersect {s3, len(s3)}')
    return len(s3) > 0


def get_smile(txt = ':kissing_heart:'):
    smile = emojize(txt, use_aliases=True)
    return smile


def get_random_smile():
    smile = choice(credentials.USER_EMOJI)
    smile = emojize(smile, use_aliases=True)
    return smile


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


def get_user_counter(user_data):

    if 'counter' not in user_data:
        user_data['counter'] = 1

    elif user_data['counter'] > 3:
        user_data['counter'] = -3

    else:
        user_data['counter'] += 1

    user_data['time'] = time.time()
    # print(f'User counter {user_data["counter"]}')
    print(user_data)
    return user_data['counter']


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

    elif is_it_intersect(credentials.CATS_DICT, norm_message):
        meaning = 'cat'

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

    elif 'шахматы' in norm_message:
        meaning = 'chess'

    print(f'meaning {meaning}')
    return meaning


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
                message = '\n'.join(weather_list)
            except (IndexError, TypeError):
                print('Weather mistake!')
                message = 'При определении погоды возникли ошибки'
    else:
        message = 'Сервис погоды временно недоступен'

    return message


def get_exchange(valute='Доллар США'):
    url = credentials.EXCHANGE_URL
    response = requests.get(url)
    root = etree.fromstring(response.content)
    for elem in root.getchildren():
        if elem[3].text == valute:
            current_course = float(elem[4].text.replace(',', '.'))
            break
    return current_course


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

    send_text(update, context, message)


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Покажи котика', 'Покажи сметанку'],
        ['Курс доллара', 'Что с погодой'],
        [KeyboardButton('Мои координаты', request_location=True), KeyboardButton('Мои контакты', request_contact=True)]
    ])
