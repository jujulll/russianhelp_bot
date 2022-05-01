import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import random
import wikipedia, re

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

word = []
i = -1

def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext=ny.content[:1000]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2

    except Exception as e:
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
    update.message.reply_text(
        f'Ваше слово: {update.message.text}\n'
        "Чем я могу помочь?",
        reply_markup=markup_act
    )
    word.append(update.message.text)
    i += 1



def check(update, context):
    update.message.reply_text(
        "777",
        reply_markup=markup_act
    )


def meaning(update, context):
    update.message.reply_text(
        getwiki(word[i]),
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
    update.message.reply_text(
        "]]]",
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