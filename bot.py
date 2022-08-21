import telebot
from telebot import types
import sqlite3 as sq

token = '5547925519:AAFcNbmPiXaDu_XfBKY3NyYv1vfiGkyMu3M'
bot = telebot.TeleBot(token)

user_data = ""
user_id = ""

@bot.message_handler(commands=['start', 'help'])
def vibor(message):
    photo = open('foto_zastavka.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, "Я бот который поможет вам купить здоровую и полезную микрозелень. "
        "Цены: горох - 100руб./100гр., подсолнух - 150руб./100гр., редис - 200руб./100гр.")

    # менюшка кнопок с выбором продукта
    markup = types.InlineKeyboardMarkup(row_width=3)
    goroh = types.InlineKeyboardButton('Горох', callback_data='goroh1')
    podsolhuh = types.InlineKeyboardButton('Подсолнух', callback_data='podsolhuh1')
    redis = types.InlineKeyboardButton('Редис', callback_data='redis1')
    markup.add(goroh, podsolhuh, redis)
    bot.send_message(message.chat.id, 'Выбирете продукт:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def menu(call):
# менюшка кнопок с выбором порции
    markup2 = types.InlineKeyboardMarkup(row_width=3)
    gr_100 = types.InlineKeyboardButton('100 гр.', callback_data='gr_100')
    gr_500 = types.InlineKeyboardButton('500 гр.', callback_data='gr_500')
    gr_1000 = types.InlineKeyboardButton('1000 гр.', callback_data='gr_1000')
    markup2.add(gr_100, gr_500, gr_1000)

# выбор продукта
    if call.message != True:
        if call.data != 'goroh1' or 'podsolhuh1' or 'redis1':
            bot.send_message(call.message.chat.id, 'Сделайте свой выбор')
        elif call.data == 'goroh1':
            photo1 = open('goroh.jpg', 'rb')
            bot.send_photo(call.message.chat.id, photo1)
            bot.send_message(call.message.chat.id, 'Выберете вашу порцию:', reply_markup=markup2)
        elif call.data == 'podsolhuh1':
            photo2 = open('podsolnuh.jpg', 'rb')
            bot.send_photo(call.message.chat.id, photo2)
            bot.send_message(call.message.chat.id, 'Выберете вашу порцию:', reply_markup=markup2)
        elif call.data == 'redis1':
            photo3 = open('redis.jpg', 'rb')
            bot.send_photo(call.message.chat.id, photo3)
            bot.send_message(call.message.chat.id, 'Выберете вашу порцию:', reply_markup=markup2)
# выбор веса
        elif call.data == 'gr_100':
            bot.send_message(call.message.chat.id, 'Для заказа введите ваше Имя и номер телефона:')
            bot.register_next_step_handler(call.message, last_answ)
            bot.register_next_step_handler(call.message, reg_data)
        elif call.data == 'gr_500':
            bot.send_message(call.message.chat.id, 'Для заказа введите ваше Имя и номер телефона:')
            bot.register_next_step_handler(call.message, last_answ)
            bot.register_next_step_handler(call.message, reg_data)
        elif call.data == 'gr_1000':
            bot.send_message(call.message.chat.id, 'Для заказа введите ваше Имя и номер телефона:')
            bot.register_next_step_handler(call.message, last_answ)
            bot.register_next_step_handler(call.message, reg_data)
    else:
        bot.send_message(call.message.chat.id, 'Сделайте свой выбор')

@bot.message_handler(content_types=['text'])
def last_answ(message):
    bot.send_message(message.chat.id, 'Спасибо. Ваш заказ принят. Менеджер перезвонит вам.')

#ввод данных в БД
def reg_data(message):
    user_data = message.text
    user_id = int(message.chat.id)

    with sq.connect('bot_order.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS user_orders(data TEXT, id INTEGER)""")
        cur.execute(f"INSERT INTO user_orders(data, id) VALUES('{user_data}', '{user_id}')")
        con.commit()

bot.polling(none_stop=True, interval=0)