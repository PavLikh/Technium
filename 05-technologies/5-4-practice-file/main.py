import json
import csv

with open('students.json', 'r', encoding="utf-8") as jsonfile:
    data = json.load(jsonfile)
    
def get_by_max_age(data: list[dict]) -> str | None:
    if not data:
        return None

    res = data[0]
    for item in data:
        if item['возраст'] > res['возраст']:
            res = item
    return f"Имя; {res['имя']}, возраст: {res['возраст']}, город: {res['город']}"

def count_by_subject(subj: str, data: list[dict]) -> int | None:
    if not data:
        return None

    count = 0
    for item in data:
        if subj.lower() in [x.lower() for x in item['предметы']]:
            count += 1
    return count

print('Общее кол-во стундетов:', len(data))
print(get_by_max_age(data))
print('Количество студентов изучающих python:', count_by_subject('python', data))