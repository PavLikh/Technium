import telebot
import os
from datetime import datetime, timedelta
from telebot import types
from db import users, sleep_records, notes, db

TOKEN = os.getenv('TG_TOKEN')
BUTTON_SLEEP = 'Спокойной ночи'
BUTTON_WAKE = 'Доброе утро'
BUTTON_REPORT = 'Отчет'
SUCCESS = 'success'
ERROR = 'error'

bot = telebot.TeleBot(TOKEN)
   
@bot.message_handler(commands=['start'])
def start(m):
    print('START BOT')
    # проверяю/создаю юзера
    users.ensure_exists(m.from_user.id, m.from_user.first_name)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(BUTTON_SLEEP)
    markup.add(button1)
    bot.send_message(m.chat.id, 'Привет! Я буду помогать тебе отслеживать параметры сна',  reply_markup=markup)
    # проверяю текущее состояние
    if sleep_records.get_is_active(m.from_user.id):
        bot.send_message(m.chat.id,'Сон еще не заверщен, завершить сон /wake',reply_markup=markup)
    else:
        bot.send_message(m.chat.id, 'Используй команды /sleep, /wake, /quality, /note, /report',  reply_markup=markup)

def handle_sleep(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(BUTTON_WAKE)
    markup.add(button)

    if sleep_records.get_is_active(m.from_user.id):
        bot.send_message(m.chat.id,'Сон еще не заверщен, завершить сон /wake',reply_markup=markup)
        return

    sleep_records.insert_row({
        "user_id": m.from_user.id,
        "sleep_time": datetime.now().isoformat()
    })
    bot.send_message(m.chat.id,'Спокойной ночи! Не забудь сообщить мне когда проснешься /wake',reply_markup=markup)


@bot.message_handler(commands=['sleep'])
def sleep(m):
    handle_sleep(m)


def handle_duration(user_id):
    active_sleep = sleep_records.get_is_active(user_id)

    if active_sleep is None:
        return ['Нет записи о начале сна. Используй /sleep, чтобы начать учёт.', ERROR]
    
    try:
        start_time = datetime.fromisoformat(active_sleep['sleep_time'])
        duration = datetime.now() - start_time
    except (ValueError, TypeError) as e:
        return ['Упс, что-то пошло не так с временем сна.', ERROR]

    if duration.days < 0:
        return ['Упс, что-то пошло не так', ERROR]
    elif duration.days > 0:
        return ['Очень длинный сон, возможно в прошлый раз мне не сообщили о пробуждении', ERROR]
    elif duration.seconds < 3600:
        mes = 'Похоже на короткий отдых, сон длился: ' + str(round(duration.seconds / 60)) + ' мин /sleep.'
    else:
        hours = round(duration.total_seconds() / 3600)
        mes = 'Доброе утро! Сон длился: ' + str(round(hours)) + ' ч /sleep.'

    return [mes + ' Не забудь оценить качество сна /quality и оставить заметки /note, отчет /report', SUCCESS]


def handle_wake(m):
    user_id = m.from_user.id
    active_sleep = sleep_records.get_is_active(user_id)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

    if active_sleep is None:
        button = types.KeyboardButton(BUTTON_SLEEP)
        markup.add(button)
        bot.send_message(m.chat.id, 'Нет сообщения о начале сна. Используй команду /sleep', reply_markup=markup)
        return

    duration = handle_duration(user_id)
    if duration[1] == SUCCESS:
        button1 = types.KeyboardButton(BUTTON_WAKE)
    else:
        button1 = types.KeyboardButton(BUTTON_SLEEP)

    button2 = types.KeyboardButton(BUTTON_REPORT)
    markup.add(button1, button2)
    bot.send_message(m.chat.id, duration[0], reply_markup=markup)
    sleep_records.update_row({
        "id": active_sleep["id"],
        "wake_time": datetime.now().isoformat()
    })


@bot.message_handler(commands=['wake'])
def wake(m):
    handle_wake(m)


@bot.message_handler(commands=['quality'])
def quality(m):
    user_id = m.from_user.id
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

    if sleep_records.get_last_sleep(user_id) is None:
        button = types.KeyboardButton(BUTTON_SLEEP)
        markup.add(button)
        bot.send_message(m.chat.id, 'Нет данных о сне. Используй команду /sleep', reply_markup=markup)
        return

    completed_sleep = sleep_records.get_is_completed(user_id)
    if completed_sleep is None:
        button = types.KeyboardButton(BUTTON_WAKE)
        markup.add(button)
        bot.send_message(m.chat.id, 'Сон не завершен. Используй команду /wake', reply_markup=markup)
        return

    if len(m.text.split()) != 2 or not m.text.split()[1].isnumeric() or not 0 < int(m.text.split()[1]) < 11:
        mes = 'Чтобы оценить сон используй команду /quality и число от 1 до 10'
    else:
        if completed_sleep['sleep_quality'] is None:
            sleep_records.update_row({
                 "id": completed_sleep["id"],
                "sleep_quality": int(m.text.split()[1])
            })
            mes = 'Оценка принята. Оставить заметку /note'
        else:
            mes = 'Уже есть оценка качества сна. Оставить заметку /note, новый сон /sleep, отчет /report'

    button1 = types.KeyboardButton(BUTTON_SLEEP)
    button2 = types.KeyboardButton(BUTTON_REPORT)
    markup.add(button1, button2)
    bot.send_message(m.chat.id, mes, reply_markup=markup)


@bot.message_handler(commands=['note'])
def handle_note(m):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_id = m.from_user.id

    if sleep_records.get_last_sleep(user_id) is None:
        button = types.KeyboardButton(BUTTON_SLEEP)
        markup.add(button)
        bot.send_message(m.chat.id, 'Нет данных о сне. Используй команду /sleep', reply_markup=markup)
        return
    
    completed_sleep = sleep_records.get_is_completed(user_id)
    if completed_sleep is None:
        button = types.KeyboardButton(BUTTON_WAKE)
        markup.add(button)
        bot.send_message(m.chat.id, 'Сон не завершен. Используй команду /wake', reply_markup=markup)
        return

    note = str(m.text).replace('/note', '')
    if len(note.strip()) < 2:
        mes = 'Введите не менее 2х символов /note'
    else:
        if notes.get_note(completed_sleep['id']) is None:
            notes.insert_row({
                "text": note,
                "sleep_record_id": completed_sleep['id']
            })
            mes = 'Заметка сохранена. Новый сон /sleep, отчет /report'
        else:
            mes = 'Уже есть заметка. Новый сон /sleep, отчет /report'

    button1 = types.KeyboardButton(BUTTON_SLEEP)
    button2 = types.KeyboardButton(BUTTON_REPORT)
    markup.add(button1, button2)
    bot.send_message(m.chat.id, mes, reply_markup=markup)


def handle_report(m):
    user_id = m.from_user.id
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    rows = sleep_records.get_all_for_user(user_id)
    if not rows:
        button = types.KeyboardButton(BUTTON_SLEEP)
        markup.add(button)
        bot.send_message(m.chat.id, 'Нет данных о сне /sleep', reply_markup=markup)
        return

    if sleep_records.get_is_active(user_id) is None:
        button = types.KeyboardButton(BUTTON_WAKE)
    else:
        button = types.KeyboardButton(BUTTON_SLEEP)
    markup.add(button)

    durations = []
    qualities = []
    
    for row in rows:
        sleep_time = row['sleep_time']
        wake_time = row['wake_time']
        quality = row['sleep_quality']
        try:
            s = datetime.fromisoformat(sleep_time)
            w = datetime.fromisoformat(wake_time)
            delta_sec = int((w - s).total_seconds())
            if delta_sec > 0:
                durations.append(delta_sec)
        except Exception:
            pass

        if quality is not None:
            qualities.append(quality)

    if len(durations) > 1:
        aver = sum(durations) / len(durations) / 3600

        q_mes = ''
        if qualities:
            if len(rows)/len(qualities) < 0.7:
                q_mes = ' Не полные данные по качеству сна, для более точных рекомендаций, лучше оценивать каждый сон'
            elif sum(qualities)/len(qualities) < 7:
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

@bot.message_handler(commands=['note'])
def note(m):
    handle_note(m)

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


try:
    bot.polling(none_stop=True)
finally:
    db.close_connect()