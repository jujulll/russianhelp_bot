import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import random
import wikipedia, re
from pymorphy2 import MorphAnalyzer

gram = {'POST': 'часть речи', 'NOUN': 'имя существительное', 'ADJF': 'имя прилагательное (полное)',
        'ADJS': 'имя прилагательное (краткое)', 'COMP': 'компаратив', 'VERB': 'глагол (личная форма)',
        'INFN': 'глагол (инфинитив)', 'PRTF': 'причастие (полное)', 'PRTS': 'причастие (краткое)',
        'GRND': 'деепричастие', 'NUMR': 'числительное', 'ADVB': 'наречие', 'NPRO': 'местоимение-существительное',
        'PRED': 'предикатив', 'PREP': 'предлог', 'CONJ': 'союз', 'PRCL': 'частица', 'INTJ': 'междометие',
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
        'incl': 'говорящий включён (идем, идемте)', 'excl': 'говорящий не включён в действие (иди, идите)',
        'VOic': 'категория залога', 'actv': 'действительный залог', 'pssv': 'страдательный залог',
        'Infr': 'разговорное', 'Slng': 'жаргонное', 'Arch': 'устаревшее', 'Litr': 'литературный вариант',
        'Erro': 'опечатка', 'Dist': 'искажение', 'Ques': 'вопросительное', 'Dmns': 'указательное',
        'Prnt': 'вводное слово', 'V-be': 'форма на -ье', 'V-en': 'форма на -енен',
        'V-ie': 'форма на -и- (веселие, твердостию); отчество с -ие', 'V-bi': 'форма на -ьи',
        'Fimp': 'деепричастие от глагола несовершенного вида', 'Prdx': 'может выступать в роли предикатива',
        'Coun': 'счётная форма', 'Coll': 'собирательное числительное', 'V-sh': 'деепричастие на -ши',
        'Af-p': 'форма после предлога', 'Inmx': 'может использоваться как одуш. / неодуш.',
        'Vpre': 'Вариант предлога ( со, подо, ...)', 'Anph': 'Анафорическое (местоимение)',
        'Init': 'Инициал', 'Adjx': 'может выступать в роли прилагательного',
        'Ms-f': 'колебание по роду (м/ж/с): кофе, вольво', 'Hypo': 'гипотетическая форма слова (победю, асфальтовее)'}
gram_list = gram.keys()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

TOKEN = '5311202148:AAH6UJzLDJSseeAUepW9lJXgO7dLdAm1aXg'

wikipedia.set_lang("ru")

reply_keyboard_start = [['/start']]
markup = ReplyKeyboardMarkup(reply_keyboard_start, one_time_keyboard=False)

reply_keyboard_comm = [['/commands'], ['/new_word']]
markup_comm = ReplyKeyboardMarkup(reply_keyboard_comm, one_time_keyboard=False)

reply_keyboard_act = [['/check', '/meaning', '/history'], ['/fon', '/morf', '/end']]
markup_act = ReplyKeyboardMarkup(reply_keyboard_act, one_time_keyboard=False)

word = ''


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
        return 'В энциклопедии нет информации об этом'


def start(update, context):
    update.message.reply_text(
        "Приветствую! Я языковой бот-помощник. Для просмотра всех команд напишите /commands.\n"
        "Для просмотра инструкции напишите /help.",
        reply_markup=markup_comm
    )


def help(update, context):
    update.message.reply_text(
        "Введите нужное вам слово, а дальше выбирайте необходимое действие."
        " Бот выдаст вам информацию из проверенных источников.",
    )


def commands(update, context):
    update.message.reply_text(
        "/new_word - начало работы с новым словом;\n"
        "/check - проверка написания слова;\n"
        "/meaning - значение слова;\n"
        "/history - происхождение слова;\n"
        "/fon - фонетический разбор слова;\n"
        "/morf - морфологический разбор слова;\n"
        "/end - завершение работы.",
        reply_markup=markup_comm
    )


def begin(update, context):
    update.message.reply_text(
        "Введите слово:",
    )


def vars(update, context):
    global word
    update.message.reply_text(
        f'Ваше слово: {update.message.text}\n'
        "Чем я могу помочь?",
        reply_markup=markup_act
    )
    word = update.message.text


def check(update, context):
    update.message.reply_text(
        "777",
        reply_markup=markup_act
    )


def meaning(update, context):
    update.message.reply_text(
        getwiki(word),
        reply_markup=markup_act
    )


def history(update, context):
    update.message.reply_text(
        "...",
        reply_markup=markup_act
    )


def fon(update, context):
    update.message.reply_text(
        ",,,",
        reply_markup=markup_act
    )


def morf(update, context):
    global word
    txt_list = []
    morph = MorphAnalyzer().parse(word)
    for i in range(len(morph)):
        txt = []
        tags = morph[i].tag
        for key in gram_list:
            if key in tags:
                txt.append(gram[key])
        txt_list.append(f'{str(i + 1)}. Н.ф.: {morph[i].normal_form}; ' + ', '.join(txt))
    update.message.reply_text(
        '\n'.join(txt_list),
        reply_markup=markup_act
    )


def end(update, context):
    update.message.reply_text(
        "Рад был помочь)))",
        reply_markup=markup_comm
    )


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
    dp.add_handler(CommandHandler("history", history))
    dp.add_handler(CommandHandler("meaning", meaning))
    dp.add_handler(CommandHandler("fon", fon))
    dp.add_handler(CommandHandler("morf", morf))
    dp.add_handler(CommandHandler("end", end))

    updater.start_polling()


if __name__ == '__main__':
    main()
