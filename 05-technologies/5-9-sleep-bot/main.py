import telebot
import os
import json
from datetime import datetime, timedelta
from telebot import types

TOKEN = os.getenv('TG_TOKEN')
FILE_NAME = 'data.json'

BUTTON_SLEEP = 'Спокойной ночи'
BUTTON_WAKE = 'Доброе утро'
BUTTON_REPORT = 'Отчет'

bot = telebot.TeleBot(TOKEN)

def datetime_decoder(obj):
    if "start" in obj:
        obj["start"] = [datetime.fromisoformat(i) for i in obj["start"]]
    return obj

def write_json(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False,  default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o))


try:
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            data = {}
        else:
            data = json.loads(content, object_hook=datetime_decoder)
            data = {int(k): v for k, v in data.items()}
except FileNotFoundError:
    data = {}
   

@bot.message_handler(commands=['start'])
def start(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(BUTTON_SLEEP)
    markup.add(button1)
    bot.send_message(m.chat.id, 'Привет! Я буду помогать тебе отслеживать параметры сна',  reply_markup=markup)
    if data and data[m.from_user.id]['sleep']:
        bot.send_message(m.chat.id,'Сон еще не заверщен, завершить сон /wake',reply_markup=markup)
    else:
        bot.send_message(m.chat.id, 'Используй команды /sleep, /wake, /quality, /note, /report',  reply_markup=markup)

def handle_sleep(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(BUTTON_WAKE)
    markup.add(button)
    if m.from_user.id not in data:
        data[m.from_user.id] = {}
        data[m.from_user.id]['duration'] = []
        data[m.from_user.id]['start'] = []
        data[m.from_user.id]['quality'] = []
        data[m.from_user.id]['note'] = []
        data[m.from_user.id]['sleep'] = False

    if data[m.from_user.id]['sleep']:
        bot.send_message(m.chat.id,'Сон еще не заверщен, завершить сон /wake',reply_markup=markup)
        return

    data[m.from_user.id]['sleep'] = True
    data[m.from_user.id]['start'].append(datetime.now() - timedelta(hours=6, minutes=30))
    data[m.from_user.id]['quality'].append(None)
    data[m.from_user.id]['note'].append(None)
    bot.send_message(m.chat.id,'Спокойной ночи! Не забудь сообщить мне когда проснешься /wake',reply_markup=markup)
    write_json(data)


@bot.message_handler(commands=['sleep'])
def sleep(m):
    handle_sleep(m)


def handle_duration(user_id):
    duration = datetime.now() - data[user_id]['start'][-1]
    if duration.days < 0:
        return ['Упс, что-то пошло не так', 'error']
    elif duration.days > 0:
        return ['Очень длинный сон, возможно в прошлый раз мне не сообщили о пробуждении', 'error']
    elif duration.seconds < 3600:
        data[user_id]['duration'].append(duration.seconds)
        mes = 'Похоже на короткий отдых, сон длился: ' + str(round(duration.seconds / 60)) + ' мин /sleep.'
    else:
        data[user_id]['duration'].append(duration.seconds)
        mes = 'Доброе утро! Сон длился: ' + str(round(duration.days * 3600 + duration.seconds / 3600)) + ' ч /sleep.'
    data[user_id]['sleep'] = False
    return [mes + ' Не забудь оценить качество сна /quality и оставить заметки /note, отчет /report', 'succes']


def handle_wake(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    if not m.from_user.id in data or not data[m.from_user.id]['sleep']:
        button = types.KeyboardButton(BUTTON_SLEEP)
        markup.add(button)
        bot.send_message(m.chat.id, 'Нет сообщения о начале сна. Используй команду /sleep', reply_markup=markup)
        return

    duration = handle_duration(m.from_user.id)
    if duration[1] == 'success':
        button1 = types.KeyboardButton(BUTTON_WAKE)
    else:
        button1 = types.KeyboardButton(BUTTON_SLEEP)

    button2 = types.KeyboardButton(BUTTON_REPORT)
    markup.add(button1, button2)
    bot.send_message(m.chat.id, duration[0], reply_markup=markup)
    write_json(data)


@bot.message_handler(commands=['wake'])
def wake(m):
    handle_wake(m)


@bot.message_handler(commands=['quality'])
def quality(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

    if not m.from_user.id in data:
        button = types.KeyboardButton(BUTTON_SLEEP)
        markup.add(button)
        bot.send_message(m.chat.id, 'Нет данных о сне. Используй команду /sleep', reply_markup=markup)
        return
    
    if data[m.from_user.id]['sleep']:
        button = types.KeyboardButton(BUTTON_WAKE)
        markup.add(button)
        bot.send_message(m.chat.id, 'Сон не завершен. Используй команду /wake', reply_markup=markup)
        return

    if len(m.text.split()) != 2 or not m.text.split()[1].isnumeric() or not 0 < int(m.text.split()[1]) < 11:
        mes = 'Чтобы оценить сон используй команду /quality и число от 1 до 10'
    else:
        if not data[m.from_user.id]['quality'][-1]:
            data[m.from_user.id]['quality'][-1] = int(m.text.split()[1])
            mes = 'Оценка принята. Оставить заметку /note'
        else:
            mes = 'Уже есть оценка качества сна. Оставить заметку /note, новый сон /sleep, отчет /report'

    button1 = types.KeyboardButton(BUTTON_SLEEP)
    button2 = types.KeyboardButton(BUTTON_REPORT)
    markup.add(button1, button2)
    bot.send_message(m.chat.id, mes, reply_markup=markup)
    write_json(data)

@bot.message_handler(commands=['note'])
def note(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

    if not m.from_user.id in data:
        button = types.KeyboardButton(BUTTON_SLEEP)
        markup.add(button)
        bot.send_message(m.chat.id, 'Нет данных о сне. Используй команду /sleep', reply_markup=markup)
        return
    
    if data[m.from_user.id]['sleep']:
        button = types.KeyboardButton(BUTTON_WAKE)
        markup.add(button)
        bot.send_message(m.chat.id, 'Сон не завершен. Используй команду /wake', reply_markup=markup)
        return

    note = str(m.text).replace('/note', '')
    if len(note.strip()) < 2:
        mes = 'Введите не менее 2х символов /note'
    else:
        if not data[m.from_user.id]['note'][-1]:
            data[m.from_user.id]['note'][-1] = note
            mes = 'Заметка сохранена. Новый сон /sleep, отчет /report'
        else:
            mes = 'Уже есть оценка качества сна. Новый сон /sleep, отчет /report'

    button1 = types.KeyboardButton(BUTTON_SLEEP)
    button2 = types.KeyboardButton(BUTTON_REPORT)
    markup.add(button1, button2)
    bot.send_message(m.chat.id, mes, reply_markup=markup)
    write_json(data)


def handle_report(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    if not m.from_user.id in data:
        button = types.KeyboardButton(BUTTON_SLEEP)
        markup.add(button)
        bot.send_message(m.chat.id, 'Нет данных о сне /sleep', reply_markup=markup)
        return

    if data[m.from_user.id]['sleep']:
        button = types.KeyboardButton(BUTTON_WAKE)
    else:
        button = types.KeyboardButton(BUTTON_SLEEP)
    markup.add(button)

    if len(data[m.from_user.id]['duration']) > 1:
        aver = sum(data[m.from_user.id]['duration']) / len(data[m.from_user.id]['duration']) / 3600

        q = [i for i in data[m.from_user.id]['quality'] if i is not None]
        q_mes = ''
        if q:
            if len(q)/len(data[m.from_user.id]['quality']) < 0.7:
                q_mes = ' Не полные данные по качеству сна, для более точных рекомендаций, лучше оценивать каждый сон'
            elif sum(q)/len(q) < 7:
                q_mes = ' Нужно повысить качество сна'
            else:
                q_mes = ' Качества сна хорошее'
        
        if aver < 1:
            bot.send_message(m.chat.id, 'Очень короткий сон или неверные данные', reply_markup=markup)
            return
        elif aver < 8:
            mes = 'Средний сон менее 8 часов, старайтесь выделить больше времени на отдых.'
        else:
            mes = 'Средний сон более 8 часов.'
        
        bot.send_message(m.chat.id, mes + q_mes, reply_markup=markup)
    else:
        bot.send_message(m.chat.id, 'Недостаточно данных', reply_markup=markup)


@bot.message_handler(commands=['report'])
def report(m):
    handle_report(m)


@bot.message_handler(content_types=["text"])
def handle_text(m):
    if m.text == BUTTON_SLEEP:
        handle_sleep(m)
    elif m.text == BUTTON_WAKE:
        handle_wake(m)
    elif m.text == BUTTON_REPORT:
        handle_report(m)


bot.polling()