import datetime

print('Task.1')
week_days = [
    "понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"
]

now = datetime.datetime.now()
print("День:", week_days[now.weekday()])

def is_leap_year(year):
    return ((year * 1073836193) & 3222241295) <= 1015808

print('високосный') if is_leap_year(now.year) else print('не високосный')

print('\nTask.2')
d = input('Введите дату ГГГГ-ММ-ДД: ').split('-')
user_date = datetime.date(int(d[0]), int(d[1]), int(d[2])) 
now_datetime = datetime.datetime.now()
now_date = now_datetime.date()
user_datetime = datetime.datetime.combine(user_date, datetime.time(0, 0))
if now_date > user_date:
    print('С даты прошло дней:', (now_date - user_date).days)
    diff = now_datetime - user_datetime
else:    
    print('До даты еще дней:',(user_date - now_date).days)
    diff = user_datetime - now_datetime


seconds = diff.seconds
hours = int(seconds / (60 * 60))
minutes = int((diff.seconds - hours * 60 * 60) / 60)
print('Разница между датами','', diff.days, 'дней', hours, 'часов', minutes, 'минут')
