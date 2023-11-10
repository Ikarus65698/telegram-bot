from telebot import types
from telebot.types import ReplyKeyboardRemove
import telebot
import numpy as np
import matplotlib.pyplot as plt
import io
import text_formation as tf

token = '5664491122:AAFsGIOEAz1E1eE2Z49Mu9vn-H34vVqCzT8'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):

    sticker_id = "CAACAgIAAxkBAAEKuS9lTcrV_0LKj84AAS71ej8-xk3427UAAtMVAAK2xjFLF3rJuNg4T3IzBA"

    bot.send_sticker(message.chat.id, sticker_id)
    bot.send_message(message.chat.id, 'Привет!')

    message_reply(message)

@bot.message_handler(content_types='text')
def message_reply(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    graph_button = types.KeyboardButton("График")
    trans_button = types.KeyboardButton('Транслит')
    markup.add(graph_button)
    markup.add(trans_button)

    bot.send_message(message.chat.id, 'Выбери необходимое тебе действие: \n1) Построить график. \n2) Транслировать текст.', reply_markup=markup)

    if (message.text.lower()=="график") or (message.text=="1") or (message.text.lower()=="построить график"):
        send_graph(message)

    elif (message.text.lower()=="транслит") or (message.text == "2"):
        translation_from_eng_or_rus(message)

@bot.message_handler(commands=['graph'])
def send_graph(message):

    bot.send_message(message.chat.id, 'Введите функцию: \nПример: 1) x^2 = y \n2) sin(x) = y', reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_function)

def get_function(message):
    func = message.text
    bot.send_message(message.chat.id, 'Введите диапазон для x: \nПример: 1) 10 \n2) -1, 5, 10, 3')
    bot.register_next_step_handler(message, get_diapason, func)

def get_diapason(message, func):

    diapason = message.text

    plt.figure(figsize=(10, 5))

    plt.plot(tf.convert_to_range(diapason), tf.transform_to_func(diapason, tf.take_parametr(func)[0]), color='green', marker='o', markersize=3)
    plt.legend(tf.take_parametr(func), fontsize=12, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, title='Функции')

    plt.xlabel('Ось x')
    plt.ylabel('Ось y')
    plt.title('Ваш график.')
    plt.grid(which='major')
    ax = plt.gca()    
    ax.axhline(y=0, color='k')  
    ax.axvline(x=0, color='k')
    plt.tight_layout()

    image_graph = io.BytesIO()
    plt.savefig(image_graph, format='png')
    image_graph.seek(0)

    bot.send_photo(message.chat.id, photo=image_graph)

    message_reply(message)

@bot.message_handler(commands=['translit'])
def translation_from_eng_or_rus(message):

    bot.send_message(message.chat.id, "Введите текст который необходимо преобразовать: \nВнимание:символы '.' и ',' будут переведены с английской раскладки как 'ю' и 'б' соответственно, учитывайте это.", reply_markup=ReplyKeyboardRemove())

    bot.register_next_step_handler(message, translit_work)

def translit_work(message):

    new_text = tf.translit(message.text)
    bot.send_message(message.chat.id, new_text)

    message_reply(message)

bot.infinity_polling()
    
