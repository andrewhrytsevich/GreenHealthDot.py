import telebot
from telebot import types
import sqlite3 as sq

token = '5547925519:AAFcNbmPiXaDu_XfBKY3NyYv1vfiGkyMu3M'
bot = telebot.TeleBot(token)

product = ""
ves = ""


def menu1():
    markup = types.InlineKeyboardMarkup(row_width=3)
    goroh = types.InlineKeyboardButton('Горох', callback_data='goroh1')
    podsolhuh = types.InlineKeyboardButton('Подсолнух', callback_data='podsolhuh1')
    redis = types.InlineKeyboardButton('Редис', callback_data='redis1')
    markup.add(goroh, podsolhuh, redis)
    return markup


def menu2():
    # менюшка кнопок с выбором порции
    markup2 = types.InlineKeyboardMarkup(row_width=3)
    gr_100 = types.InlineKeyboardButton('100 гр.', callback_data='gr_100')
    gr_500 = types.InlineKeyboardButton('500 гр.', callback_data='gr_500')
    gr_1000 = types.InlineKeyboardButton('1000 гр.', callback_data='gr_1000')
    markup2.add(gr_100, gr_500, gr_1000)
    return markup2


@bot.message_handler(commands=['start'])
def vibor(message):
    photo = open('foto_zastavka.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, "Я бот который поможет вам купить здоровую и полезную микрозелень. "
                                      "Цены: горох - 100руб./100гр., подсолнух - 150руб./100гр., редис - 200руб./100гр.")
    bot.send_message(message.chat.id, 'Выбирете продукт:', reply_markup=menu1())


@bot.callback_query_handler(
    func=lambda call: call.data == 'goroh1' or call.data == 'podsolhuh1' or call.data == 'redis1', )
def menu_product(call):
    # выбор продукта
    if call.data == 'goroh1':
        photo1 = open('goroh.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo1)
        bot.send_message(call.message.chat.id, 'Выберете вашу порцию:', reply_markup=menu2())
    elif call.data == 'podsolhuh1':
        photo2 = open('podsolnuh.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo2)
        bot.send_message(call.message.chat.id, 'Выберете вашу порцию:', reply_markup=menu2())
    elif call.data == 'redis1':
        photo3 = open('redis.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo3)
        bot.send_message(call.message.chat.id, 'Выберете вашу порцию:', reply_markup=menu2())
    global product
    product = call.data


@bot.callback_query_handler(func=lambda call: call.data == 'gr_100' or call.data == 'gr_500' or call.data == 'gr_1000')
def menu_ves(call):
    # выбор веса
    if call.data in ['gr_100', 'gr_500', 'gr_1000']:
        bot.send_message(call.message.chat.id, 'Для заказа введите ваше Имя и номер телефона:')
        bot.register_next_step_handler(call.message, last_answ)
        bot.register_next_step_handler(call.message, reg_data)
    global ves
    ves = call.data


@bot.message_handler(content_types=['text'])
def last_answ(message):
    if product and ves:
        bot.send_message(message.chat.id, 'Спасибо. Ваш заказ принят. Менеджер перезвонит вам.')
    else:
        bot.send_message(message.chat.id, 'Вы не сделали свой выбор. Нажмите нужную кнопку.')


# ввод данных в БД
def reg_data(message):
    user_data = message.text
    user_id = int(message.chat.id)
    global ves
    global product
    with sq.connect('bot_order.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS user_orders(data TEXT, id INTEGER, product TEXT, ves TEXT)""")
        cur.execute(
            f"INSERT INTO user_orders(data, id, product, ves) VALUES('{user_data}', '{user_id}', '{product}', '{ves}')")
        con.commit()


bot.polling(none_stop=True, interval=0)
