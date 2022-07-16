import os

import telebot
import flask
import requests
import nltk
import random
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, CallbackContext, MessageHandler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#TOKEN =
#APP_URL =
#bot = telebot.TeleBot(TOKEN)
####if __name__ == '__main__':
    #server.run(host='0.0.0.0.', port = int(os.environ.get('PORT', 5000 )))

bot = Bot(token='5535285847:AAGXWzIDSVTAwyTTgpWj06PXJup1ge-ucxU')
dp = Dispatcher(bot)
with open('BIG_BOT_CONFIG.json', 'r') as f:
    BOT_CONFIG = json.load(f)

def cleaner(text):
    cleaned_text = ''
    for i in text.lower() :
        if i in "qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъэждлорпавыфячсмитьбю ":
            cleaned_text = cleaned_text + i

    return cleaned_text

def match(text, example):
    return nltk.edit_distance(text, example) / len(example) < 0,4 if len(example) > 0 else False

def get_intent(text):
    global intent
    for intent in BOT_CONFIG [ 'intents' ]:
        if 'examples' in BOT_CONFIG [ 'intents' ] [ intent ]:
            for example in BOT_CONFIG [ 'intents' ] [ intent ] [ 'examples' ]:
                if match(cleaner (text), cleaner (example)):
                    return intent


X=[]
Y=[]

for intent in BOT_CONFIG ['intents']:
    if 'examples' in BOT_CONFIG['intents'] [intent]:
        X += BOT_CONFIG['intents'] [intent] ['examples']
        Y += [intent for i in range(len(BOT_CONFIG['intents'] [intent] ['examples']))]

vectorizer = CountVectorizer(preprocessor=cleaner, ngram_range=[1, 4], stop_words=['a', 'и'])

vectorizer.fit(X)
X_vect= vectorizer.transform(X)

X_train_vect, X_test_vect,Y_train, Y_test = train_test_split(X_vect, Y, test_size=0.4)

sgd = SGDClassifier()
sgd.fit(X_vect, Y)
sgd.score(X_vect, Y)

def get_intent_model(text):
    return sgd.predict(vectorizer.transform([text]))[0]


def bot(text):  # функция бота
    global intent
    intent = get_intent(text)  # Пытаемся понять намерение и сравнить по Левенштейну

    if intent is None:
        intent = get_intent_model(text)  # пытаемся понять намерение с помощью ML модели

    print(intent)
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])
    # Возвращаем рандомный ответ из определённого интента из словаря responses


logging.basicConfig(
    format='%(actime)s -  %(name)s - %(levelname)s - %(massege)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Я Бот, Гений, PlayBoy, чтобы начать диалог со мной, напиши мне "Привет"!')


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Меню /help')


def output(update: Update, _: CallbackContext) -> None:
    text = update.message.text
    print(text)
    update.message.reply_text(bot(text))


def main() -> None:
    updater = Updater("5535285847:AAGXWzIDSVTAwyTTgpWj06PXJup1ge-ucxU")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, output))

    updater.start_polling()

    updater.idle()


main()

