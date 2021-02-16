import credentials
from emoji import emojize
import glob
import logging
import pymorphy2
from pprint import pprint
import re
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)
TOKEN = credentials.TOKEN


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
    update.message.reply_text(f'Привет, попроси меня показать тебе {choice(credentials.CATS_DICT)}! {smile}')


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
    return len(s3)


def find_the_meaning(message):

    norm_message = normalized(message)

    if is_it_intersect(credentials.NAMES, norm_message):
        return 'имена'

    if ('не' in norm_message) and ('показывать' in norm_message) and \
            (('кот' in norm_message) or ('кошка' in norm_message)):
        return 'котейка плачет'

    elif ('показать' in norm_message) and (('кот' in norm_message) or ('кошка' in norm_message)):
        return 'нужно показать кота'

    elif len(list(set(credentials.CATS_DICT).intersection(set(norm_message)))):
        return 'нужно показать кота'

    elif len(list(set(credentials.COMPLIMENTS).intersection(set(norm_message)))):
        return 'тут надо умилиться'

    elif len(list(set(credentials.INSULTS).intersection(set(norm_message)))):
        return 'тут надо фыркнуть и обидеться'

    elif ('показать' in norm_message) and ('сушка' in norm_message):
        return 'показать сушку'

    elif ('показать' in norm_message) and \
            (('собака' in norm_message) or ('сметанка' in norm_message)):
        return 'показать собаку'
    elif 'сметана' in norm_message:
        return 'показать сметану'

    elif ('ромка' in norm_message) and ('настоящий' in norm_message):
        return 'настоящего ромку'

    elif 'ромка' in norm_message:
        return 'показать бородатого'


    else:
        return 'не определен'


def echo_text(update, context):

    message = update.message.text
    chat_id = update.effective_chat.id
    print(chat_id, message)

    meaning = find_the_meaning(message)
    if meaning == 'имена':
        context.bot.send_photo(chat_id=chat_id, photo=open(glob.glob('images/names.jpg')[0], 'rb'))
        return

    if meaning == 'показать бородатого':
        bearded = glob.glob('images/rom.jpg')[0]
        context.bot.send_photo(chat_id=chat_id, photo=open(bearded, 'rb'))
        return

    if meaning == 'настоящего ромку':
        real_rom = glob.glob('images/real_rom.jpg')[0]
        print(real_rom)
        context.bot.send_photo(chat_id=chat_id, photo=open(real_rom, 'rb'))
        return

    if meaning == 'тут надо умилиться':
        update.message.reply_text(f'Мяy-мяy {get_smile()}')
        return

    if meaning == 'тут надо фыркнуть и обидеться':
        update.message.reply_text(f'Фррр {get_smile(":smirk_cat:")}')
        return

    if meaning == 'нужно показать кота':
        send_cat(update, context)
        return

    if meaning == 'показать сушку':
        send_sushka(update, context)
        return

    if meaning == 'показать собаку':
        send_dog(update, context)
        return

    if meaning == 'показать сметану':
        send_cream(update, context)
        return
    # for cat in CATS_DICT:
    #     if cat in message:
    #         send_cat(update, context)
    #         return

    # for compliment in credentials.COMPLIMENTS:
    #     if compliment in message.lower():
    #         update.message.reply_text(f'Мяy-мяy {get_smile()}')
    #         return

    # for insult in credentials.INSULTS:
    #     if insult in message.lower():
    #         update.message.reply_text(f'Фррр {get_smile(":smirk_cat:")}')
    #         return


def send_cream(update, context):
    print('cream send activate')
    cream_photos_list = glob.glob('images/*cream*')
    cream_photo = choice(cream_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cream_photo, 'rb'))

def send_cat(update, context):
    print('cats')
    cat_photos_list = glob.glob('images/*cat*')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def send_sushka(update, context):
    print('sushka activated')
    sushka_filename = glob.glob('images/sushka.jpeg')[0]
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(sushka_filename, 'rb'))


def send_dog(update, context):
    print('smetanka activated')
    dogs_list = glob.glob('images/*dog*.jp*g')
    dog_filename = choice(dogs_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(dog_filename, 'rb'))


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



