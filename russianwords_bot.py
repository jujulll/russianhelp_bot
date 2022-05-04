# здесь написаны пути до бд (переменная path_to_db в 57 строке)
# и папки с мемами (переменная path_to_dir_of_mems в 58 строке)
# (чтобы каждый раз не искать, а скопировать отсюда и вставить в нужную переменную)
# путь до бд Юля: D:/pythonProject2/russian bot
# путь до бд Женя: C:/Users/detec/PycharmProject/yandex_and_kirienko179/words_of_users.sqlite
# путь до ПАПКИ с мемами Юля: D:/pythonProject2/mems
# путь до ПАПКИ с мемами Женя: C:/Users/detec/PycharmProject/yandex_and_kirienko179/mems

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from random import randint
import wikipedia, re, requests, sqlite3
from pymorphy2 import MorphAnalyzer
import json

gram = {'POST': 'часть речи', 'NOUN': 'имя существительное', 'ADJF': 'имя прилагательное (полное)',
        'ADJS': 'имя прилагательное (краткое)', 'COMP': 'компаратив', 'VERB': 'глагол (личная форма)',
        'INFN': 'глагол (инфинитив)', 'PRTF': 'причастие (полное)', 'PRTS': 'причастие (краткое)',
        'GRND': 'деепричастие', 'NUMR': 'числительное', 'ADVB': 'наречие', 'NPRO': 'местоимение-существительное',
        'PRED': 'предикатив', 'PREP': 'предлог', 'CONJ': 'союз', 'PRCL': 'частица', 'INTJ': 'междометие',
        'LATN': 'слово состоит из латинских букв', 'PNCT': 'пунктуация', 'NUMB': 'число', 'intg': 'целое число',
        'real': 'вещественное число', 'ROMN': 'римское число', 'UNKN': 'слово не удалось разобрать',
        'ANim': 'категория одушевлённости', 'anim': 'одушевлённое', 'inan': 'неодушевлённое',
        'GNdr': 'род / род не выражен', 'masc': 'мужской род', 'femn': 'женский род', 'neut': 'средний род',
        'ms-f': 'общий род (м/ж)', 'NMbr': 'число', 'sing': 'единственное число', 'plur': 'множественное число',
        'Sgtm': 'singularia tantum', 'Pltm': 'pluralia tantum', 'Fixd': 'неизменяемое', 'CAse': 'категория падежа',
        'nomn': 'именительный падеж', 'gent': 'родительный падеж', 'datv': 'дательный падеж',
        'accs': 'винительный падеж', 'ablt': 'творительный падеж', 'loct': 'предложный падеж',
        'voct': 'звательный падеж', 'gen1': 'первый родительный падеж',
        'gen2': 'второй родительный (частичный) падеж', 'acc2': 'второй винительный падеж',
        'loc1': 'первый предложный падеж', 'loc2': 'второй предложный (местный) падеж', 'Abbr': 'аббревиатура',
        'Name': 'имя', 'Surn': 'фамилия', 'Patr': 'отчество', 'Geox': 'топоним', 'Orgn': 'организация',
        'Trad': 'торговая марка', 'Subx': 'возможна субстантивация', 'Supr': 'превосходная степень',
        'Qual': 'качественное', 'Apro': 'местоименное', 'Anum': 'порядковое', 'Poss': 'притяжательное',
        'V-ey': 'форма на -ею', 'V-oy': 'форма на -ою', 'Cmp2': 'сравнительная степень на по-',
        'V-ej': 'форма компаратива на -ей', 'ASpc': 'категория вида', 'perf': 'совершенный вид',
        'impf': 'несовершенный вид', 'TRns': 'категория переходности', 'tran': 'переходный',
        'intr': 'непереходный', 'Impe': 'безличный', 'Impx': 'возможно безличное употребление',
        'Mult': 'многократный', 'Refl': 'возвратный', 'PErs': 'категория лица', '1per': '1 лицо', '2per': '2 лицо',
        '3per': '3 лицо', 'TEns': 'категория времени', 'pres': 'настоящее время', 'past': 'прошедшее время',
        'futr': 'будущее время', 'MOod': 'категория наклонения', 'indc': 'изъявительное наклонение',
        'impr': 'повелительное наклонение', 'INvl': 'категория совместности',
        'incl': 'говорящий включён в действие', 'excl': 'говорящий не включён в действие',
        'VOic': 'категория залога', 'actv': 'действительный залог', 'pssv': 'страдательный залог',
        'Infr': 'разговорное', 'Slng': 'жаргонное', 'Arch': 'устаревшее', 'Litr': 'литературный вариант',
        'Erro': 'опечатка', 'Dist': 'искажение', 'Ques': 'вопросительное', 'Dmns': 'указательное',
        'Prnt': 'вводное слово', 'V-be': 'форма на -ье', 'V-en': 'форма на -енен',
        'V-ie': 'форма на -и- или отчество с -ие', 'V-bi': 'форма на -ьи',
        'Fimp': 'деепричастие от глагола несовершенного вида', 'Prdx': 'может выступать в роли предикатива',
        'Coun': 'счётная форма', 'Coll': 'собирательное числительное', 'V-sh': 'деепричастие на -ши',
        'Af-p': 'форма после предлога', 'Inmx': 'может использоваться как одуш. / неодуш.',
        'Vpre': 'Вариант предлога', 'Anph': 'Анафорическое (местоимение)', 'Init': 'Инициал',
        'Adjx': 'может выступать в роли прилагательного', 'Ms-f': 'колебание по роду (м/ж/с)',
        'Hypo': 'гипотетическая форма слова'}
gram_list = gram.keys()
path_to_db = 'D:/pythonProject2/russian bot/words_of_users.sqlite'
path_to_dir_of_mems = 'D:/pythonProject2/russian bot/mems'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

TOKEN = '5311202148:AAH6UJzLDJSseeAUepW9lJXgO7dLdAm1aXg'

wikipedia.set_lang("ru")

reply_keyboard_start = [['/start']]
markup = ReplyKeyboardMarkup(reply_keyboard_start, one_time_keyboard=False)

reply_keyboard_comm = [['/commands', '/mem'], ['/new_word', '/TEST']]
markup_comm = ReplyKeyboardMarkup(reply_keyboard_comm, one_time_keyboard=False)

reply_keyboard_act = [['/check', '/meaning', '/morfem'], ['/fon', '/morfol', '/end']]
markup_act = ReplyKeyboardMarkup(reply_keyboard_act, one_time_keyboard=False)

reply_keyboard_answer = [['/1', '/2'], ['/3', '/4', '/5'], ['/back']]
markup_answ = ReplyKeyboardMarkup(reply_keyboard_answer, one_time_keyboard=False)

reply_keyboard_task = [['/task_4'], ['/task_5'], ['/task_6'], ['/task_7'], ['/end']]
markup_task = ReplyKeyboardMarkup(reply_keyboard_task, one_time_keyboard=False)
c_a = ""


def get_word(chat_id):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    if cur.execute(f'select word from words_of_users where from_user_id = {chat_id}').fetchall() == []:
        cur.execute(f'insert into words_of_users(from_user_id,word) values({chat_id},"привет")')
        con.commit()
        return 'привет'
    return cur.execute(f'select word from words_of_users where from_user_id = {chat_id}').fetchall()[0][0]


def send_word(chat_id, word):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    if cur.execute(f'select word from words_of_users where from_user_id = {chat_id}').fetchall() == []:
        cur.execute(f'insert into words_of_users(from_user_id,word) values({chat_id},"{word}")')
    else:
        cur.execute(f'update words_of_users set word="{word}" where from_user_id={chat_id}')
    con.commit()


def test(update, context):
    update.message.reply_text(
        "Выберите номер задания:\n"
        "4.Постановка ударения\n"
        "5.Употребление паронимов\n"
        "6.Лексические нормы\n"
        "7.Морфологические нормы (образование форм слова)",
        reply_markup=markup_task
    )


def ege(update, context):
    global c_a
    w = update.message.text[-1]
    t = ''
    r = randint(0, 5)
    with open('questions.json', encoding='UTF-8') as file:
        data = json.load(file)
    for key, value in data.items():
        if key == w:
            t = value[r]['question']
            c_a = value[r]['answer']
            break
    update.message.reply_text(t, reply_markup=markup_answ)


def check_answer(update, context):
    m = "/" + c_a[0]
    a = ""
    if update.message.text == m:
        a = "Ваш ответ верный!"
    else:
        a = "Неверно\n Правильный ответ:" + c_a[2:]
    update.message.reply_text(a, reply_markup=markup_task)


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if len((x.strip())) > 3:
                   wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        wikitext2 = re.sub('  ', ' ', wikitext2)
        return wikitext2
    except Exception:
        txts = ['Я не нашел информацию о введенном слове. Может, где-то в слове затаилась коварная ошибка? 🤔',
                'В энциклопедии нет информации об этом 😩',
                'К сожалению, я не могу найти информацию об этом слове ☹ Проверьте правильность введенного слова']
        return txts[randint(0, 2)]


def start(update, context):
    update.message.reply_text("Приветствую! 🙌 Я языковой бот-помощник. Для просмотра всех команд напишите /commands.\n"
                              "Для просмотра инструкции напишите /help.", reply_markup=markup_comm)


def help(update, context):
    update.message.reply_text("Введите нужное вам слово, а дальше выбирайте необходимое действие."
                              " Бот выдаст вам информацию из проверенных источников.")


def commands(update, context):
    update.message.reply_text("Вот список того, что я умею 😊:\n/new_word - начало работы с новым словом;\n"
                              "/check - проверка написания слова;\n/meaning - значение слова;\n"
                              "/morfem - морфемный разбор слова;\n/fon - фонетический разбор слова;\n"
                              "/morfol - морфологический разбор слова;\n/mem - отправка рандомного мема;\n"
                              "/TEST - задания из тестовой части ЕГЭ;\n"
                              "/end - завершение работы.", reply_markup=markup_comm)


def begin(update, context):
    update.message.reply_text("Введите слово:")


def vars(update, context):
    word = update.message.text
    send_word(update.message.from_user.id, word)
    update.message.reply_text(f'Ваше слово: {word}\nЧем я могу помочь? 😊', reply_markup=markup_act)


def check(update, context):
    word = get_word(update.message.from_user.id)
    if MorphAnalyzer().word_is_known(word):
        txts = ['Вы правильно написали слово! 👍', 'Такое слово нашлось в моем словаре. Должно быть, оно существует! 🤔',
                'Полагаю, вашей грамотности нет предела! 🙃']
        txt = txts[randint(0, 2)]
    else:
        txts = ['Вряд ли введенное вами слово верное. Попробуйте другой вариант написания😉',
                'Пожалуй, вам стоит попробовать написать слово по-другому🤔', 'Слова, введенного вами, в словаре нету😩']
        txt = txts[randint(0, 2)]
    update.message.reply_text(txt, reply_markup=markup_act)


def meaning(update, context):
    word = get_word(update.message.from_user.id)
    update.message.reply_text(getwiki(word), reply_markup=markup_act)


def morfem(update, context):
    word = get_word(update.message.from_user.id)
    try:
        response = requests.get(f'https://kartaslov.ru/разбор-слова-по-составу/{word}').content.decode('utf-8').\
            split('        <table class="morphemics-table-v2">')
        txts = []
        for i in response[1].split('                                    </table>')[0].\
                split('                                                                                '):
            for j in i.split('\t'):
                morfeme = j[:-32].split("<td class='td-morpheme-text'>")[1].\
                    split("</td>\n                        <td class='td-morpheme-type'>")
                if morfeme[1] == 'нулевое<br/>окончание':
                    txts.append('окончание: нулевое')
                elif morfeme[1] == 'глагольное<br/>окончание':
                	txts.append(f'глагольное окончание: {morfeme[0]}')
                else:
                    txts.append(f'{morfeme[1]}: {morfeme[0]}')
        txt = f'Лови морфемный разбор слова {word} 😊:\n' + ';\n'.join(txts)
    except Exception:
        txts = ['Извините, я не могу сделать морфемный разбор этого слова. Попробуйте другое слово 🙁',
                'Вот незадача! В моих источниках морфемного разбора такого слова не найдено 😞',
                'Мне очень жаль, но я не могу сделать морфемный разбор данного вами слова 🙁']
        txt = txts[randint(0, 2)]
    update.message.reply_text(txt, reply_markup=markup_act)


def fon(update, context):
    word = get_word(update.message.from_user.id)
    try:
        txt = f'😊 Лови фонетический разбор слова {word}: ' + requests.get(f"https://frazbor.ru/{word}").content.\
            decode("utf-8").split('\n')[63].split('<span class="transcription">')[1].split('</span></dd></dl>')[0]
        while '<' in txt and '>' in txt:
            txt = txt[:txt.index('<')] + txt[txt.index('>') + 1:]
    except Exception:
        txts = ['Извините, я не могу сделать фонетический разбор этого слова. Попробуйте другое слово 🙁',
                'Вот незадача! Нет транскрипции не существующего в моем карманном словарике слова 😞',
                'Мне очень жаль, но я не могу сделать фонетический разбор данного вами слова 🙁']
        txt = txts[randint(0, 2)]
    update.message.reply_text(txt, reply_markup=markup_act)


def morfol(update, context):
    word = get_word(update.message.from_user.id)
    txt_list = []
    morph = MorphAnalyzer().parse(word)
    for i in range(len(morph)):
        txt = []
        tags = morph[i].tag
        for key in gram_list:
            if key in tags:
                txt.append(gram[key])
        txt_list.append(f'{str(i + 1)}. Н.ф.: {morph[i].normal_form}; ' + ', '.join(txt))
    if MorphAnalyzer().word_is_known(word):
        txt = f'😉 Лови все варианты морфологического разбора слова {word}:\n' + '\n'.join(txt_list)
    else:
        txts = ['Извините, я не могу сделать морфологический разбор этого слова. Попробуйте другое слово 🙁',
                'Вот незадача! Я не могу сделать морфологический разбор несуществующего слова 😞',
                'Мне очень жаль, но я не могу сделать морфологический разбор введенного слова 🙁']
        txt = txts[randint(0, 2)]
    update.message.reply_text(txt, reply_markup=markup_act)
    print(update.message.from_user.id)


def mem(update, context):
    context.bot.send_photo(chat_id=update.message.from_user.id,
                           photo=open(f'{path_to_dir_of_mems}/mem{randint(1, 20)}.jpg', 'rb'))


def end(update, context):
    update.message.reply_text("Рад был помочь! 😊", reply_markup=markup_comm)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text & ~Filters.command, vars)
    dp.add_handler(text_handler)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("commands", commands))
    dp.add_handler(CommandHandler("new_word", begin))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("morfem", morfem))
    dp.add_handler(CommandHandler("meaning", meaning))
    dp.add_handler(CommandHandler("fon", fon))
    dp.add_handler(CommandHandler("morfol", morfol))
    dp.add_handler(CommandHandler('mem', mem))
    dp.add_handler(CommandHandler('TEST', test))
    dp.add_handler(CommandHandler('task_4', ege))
    dp.add_handler(CommandHandler('task_5', ege))
    dp.add_handler(CommandHandler('task_6', ege))
    dp.add_handler(CommandHandler('task_7', ege))
    dp.add_handler(CommandHandler('back', test))
    dp.add_handler(CommandHandler('1', check_answer))
    dp.add_handler(CommandHandler('2', check_answer))
    dp.add_handler(CommandHandler('3', check_answer))
    dp.add_handler(CommandHandler('4', check_answer))
    dp.add_handler(CommandHandler('5', check_answer))
    dp.add_handler(CommandHandler("end", end))

    updater.start_polling()


if __name__ == '__main__':
    main()