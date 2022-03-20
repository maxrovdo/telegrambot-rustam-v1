import threading
import telebot
import datetime
import time
import sqlite3
from telebot import types

bot = telebot.TeleBot('5120898350:AAGIiFskc-JAeF874l7c8GhlaXqTIWomUg4')


def write_to_bd(message):
    db = sqlite3.connect('database_telegram_bot.db')
    cursor = db.cursor()
    db.execute('''CREATE TABLE IF NOT EXISTS users(
            id, 
            first_name, 
            last_name, 
            uesrname, 
            datetime
            )''')
    db.commit()
    cursor.execute('SELECT id FROM users WHERE id == ?', (message.from_user.id,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', (
            message.from_user.id, f'{message.from_user.first_name}', f'{message.from_user.last_name}',
            f'{message.from_user.username}', f'{datetime.datetime.utcfromtimestamp(message.date + 10800)}'))
        db.commit()
    else:
        pass

    # for id in cursor.execute("SELECT id FROM users").fetchall(): # для отправки рассылки по пользователям в базе
    #     bot.send_message(id[0], 'Hello. It is test message')


@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id,
                         f'''Привет, {message.from_user.first_name} ☺\n[здесь будет первое сообщение + <a href="https://weginszoo.by/">линка</a>]''',
                         parse_mode='HTML')
        time.sleep(0.35)
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAPXYjDYB5l9MPkzFzIw1D71V2HPDhUAAmMSAAIx75lLjbqRBvc-W10jBA')

        write_to_bd(message)

        if str(message.chat.id) not in [i.strip() for i in open('chat_id.txt', 'r').readlines()]:
            with open('chat_id.txt', 'a+') as chat_id:
                print(message.chat.id, file=chat_id)
            with open('users_data.txt', 'a+') as users_data:
                print(message.chat.id, message.from_user.first_name, message.from_user.last_name,
                      message.from_user.username, datetime.datetime.utcfromtimestamp(message.date + 10800), sep=' | ',
                      file=users_data)

                bot.send_message(5253160477, f'''
    <b>Новый подписчик:</b>
    <i>id пользователя:</i>  {message.from_user.id}
    <i>Имя:</i>  {message.from_user.first_name}
    <i>Фамилия:</i>  {message.from_user.last_name}
    <i>Псевдоним:</i>  {message.from_user.username}
    <i>Время:</i>  {datetime.datetime.utcfromtimestamp(message.date + 10800)}\n''', parse_mode='HTML')

        def threading_func(a: int = 0, interval: int = 0, mes1=None, mes2=None):
            if a == 1:
                bot.send_message(message.chat.id,
                                 '[здесь будет второе сообщение + <a href="https://weginszoo.by/">линка</a>]',
                                 parse_mode='HTML')
                kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                btn1 = types.KeyboardButton('рустам хуила🤪')
                btn2 = types.KeyboardButton('рустам пидрила😇')
                btn3 = types.KeyboardButton('рустам хуегрызина😱')
                kb.add(btn1, btn2, btn3)
                mes1 = bot.send_message(message.chat.id, 'выбери подходящий вариант: 💋', reply_markup=kb)
                interval = 7200  # второе сообщение отправляется через 2 часа после первого
            if a == 2:
                bot.send_message(message.chat.id,
                                 '[здесь будет третье сообщение + <a href="https://weginszoo.by/">линка</a>]',
                                 parse_mode='HTML')
                kb1 = types.InlineKeyboardMarkup()
                btn4 = types.InlineKeyboardButton('рустам хуила🥰', url='https://www.google.com/')
                btn5 = types.InlineKeyboardButton('рустам пидрила😂', url='https://weginszoo.by/')
                btn6 = types.InlineKeyboardButton('рустам хуегрызина🥸', callback_data='1')
                btn7 = types.InlineKeyboardButton('рустам питушара😡', callback_data='2')
                kb1.row(btn4, btn5)
                kb1.row(btn6, btn7)
                mes2 = bot.send_message(message.chat.id, 'выбери самый подходящий вариант: 😎😎', reply_markup=kb1)
                interval = 18000  # третье сообщение отправляется через 5 часов после второго
            if a == 3:
                bot.send_message(message.chat.id,
                                 '[здесь будет четвертое сообщение + <a href="https://weginszoo.by/">линка</a>]',
                                 parse_mode='HTML')
                bot.delete_message(message.chat.id, mes1.id)
                bot.delete_message(message.chat.id, mes2.id)
                photo = open('photo_1.JPG', 'rb')
                bot.send_photo(message.chat.id, photo, 'О, привет!')
                interval = 60  # четвертое сообщение отправляется через 1 минуту после третьего
            if a == 4:
                bot.send_message(message.chat.id,
                                 '[здесь будет пятое сообщение + <a href="https://weginszoo.by/">линка</a>]',
                                 parse_mode='HTML')
                interval = 0
            if a == 5:
                return
            a += 1
            timer = threading.Timer(interval, threading_func, (a, interval, mes1, mes2))
            timer.start()

        threading_func(a=0, interval=900, mes1=0,
                       mes2=0)  # первое сообщение потока отправляется через 15 минут после подписки на бота
    except Exception:
        pass


bot.polling()
