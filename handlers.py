import glob
from utils import *


def greet_user(update, context):
    # update это нам передаст диспетчер там будет инфа, которую нам передал телеграм
    # context это непонятное что-то..
    print('вызван start')
    smile = get_smile(random_smile=True)
    update.message.reply_text(f'Привет, попроси меня показать тебе котика {smile}', reply_markup=main_keyboard())


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


def send_text(update, context, message=''):
    if not len(message):
        message = update.message.text
    update.message.reply_text(message)


def user_location(update, context):
    coordinates = update.message.location
    print(coordinates)
