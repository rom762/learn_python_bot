from pprint import pprint
import credentials
import re
import pymorphy2

messages = ['покажи сушку',
            'не показывай кота', 'не показывай кошку',
            'Хм.. да .. с Сушкой проблемы',
            'может быть Тёмку?',
            'какая удача',
            'Эх, не судьба Сушке',
            'Гадкий бот',
            'Плохой бот',
            'Хороший бот',
            'Умница',
            'Иди обниму',
            ]


normalized_corpus = []


def normalized(message):
    # print(f'функция normalized на вход пришло: {message}')
    regexp = r'\w+'
    regexp_compiled = re.compile(regexp)
    morph = pymorphy2.MorphAnalyzer()

    message_lower = message.lower()
    message_by_words = regexp_compiled.findall(message_lower)
    message_normalized = []
    for word in message_by_words:
        message_normalized.append(morph.normal_forms(word)[0])
    # print(f'на выходе получили {message_normalized}')
    return message_normalized


def find_the_meaning(norm_message):
    #     show cat
    if ('не' in norm_message) and ('показывать' in norm_message) and \
            (('кот' in norm_message) or ('кошка' in norm_message)):
        return 'котейка плачет'

    elif ('показать' in norm_message) and (('кот' in norm_message) or ('кошка' in norm_message)):
        return 'нужно показать кота'

    elif len(list(set(credentials.COMPLIMENTS).intersection(set(norm_message)))):
        return 'тут надо умилиться'

    elif len(list(set(credentials.INSULTS).intersection(set(norm_message)))):
        return 'тут надо фыркнуть и обидеться'
    else:
        return 'не определен'


for message in messages:
    normalized_message = normalized(message)
    normalized_corpus.append(normalized_message)

print(len(normalized_corpus))
pprint(normalized_corpus)

for message in normalized_corpus:
    print(f'исходное {message}')
    print(f'смысл: {find_the_meaning(message)}')









# на самом деле без word2vec нам не обойтись потому как нам нужно смысл анализировать.
# например нужно взять эталонные фразы типа "покажи кота", "не показывай кота" и считать векторные расстояния между ними и сообщением пользователя
# потом по наиболее совпавшим выбирать действие.
# давай сейчас накидаем план

# показать кота
#
# показать не кота
#
# обидеться
#
# умилится
#







