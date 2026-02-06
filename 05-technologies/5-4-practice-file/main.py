import json
import csv
import datetime

# task.1
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

print('1. JSON')
print('Общее кол-во стундетов:', len(data))
print(get_by_max_age(data))
print('Количество студентов изучающих python:', count_by_subject('python', data))

# task.2
with open('sales.csv', 'r', encoding="utf-8") as csvfile:
    sales = list(csv.DictReader(csvfile))

def total_amount(data: list[dict]) -> int | None:
    if not data:
        return None

    return sum(int(row['Сумма']) for row in data)

def max_sale_product(data: list[dict]) -> list | None:
    if not data:
        return None

    products = {}
    with_max_amount = [0, '']
    with_max_quan = [0, '']
    for row in data:
        if row['Продукт'] not in products:
            products[row['Продукт']] = {'count': 1, 'sum': int(row['Сумма'])}
        else:
            products[row['Продукт']]['count'] += 1
            products[row['Продукт']]['sum'] += int(row['Сумма'])
        if with_max_amount[0] < products[row['Продукт']]['sum']:
            with_max_amount[0] = products[row['Продукт']]['sum']
            with_max_amount[1] = row['Продукт']
        if with_max_quan[0] < products[row['Продукт']]['count']:
            with_max_quan[0] = products[row['Продукт']]['count']
            with_max_quan[1] = row['Продукт']
    
    return [with_max_amount, with_max_quan]

months = [
        "январь", "февраль", "март", "апрель", "май", "июнь",
        "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
    ]

def sale_by_month(data: list[dict]) -> list | None:
    if not data:
        return None
    products_by_month = {}
    
    for row in data:
        d = row['Дата'].split('-')
        date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
        if date.year not in products_by_month:
            products_by_month[date.year] = {}
            products_by_month[date.year][date.month] = int(row['Сумма'])
        else:
            if date.month not in products_by_month[date.year]:
                products_by_month[date.year][date.month] = int(row['Сумма'])
            else:
                products_by_month[date.year][date.month] += int(row['Сумма'])

    return {
        year: {months[m - 1]: value for m, value in months_data.items()}
        for year, months_data in products_by_month.items()
    }

print('\n2. CSV')
print('Общая сумма:', total_amount(sales))
report = max_sale_product(sales)
print('Товар с самым высоким объемом прдаж по количеству:', report[1][1], 'Количество:', report[1][0])
print('Товар с самым высоким объемом прдаж по сумме:', report[0][1], 'Сумма:', report[0][0])
result = sale_by_month(sales)
print('\nОбщая сумма по каждому месяцу')
for year, months in result.items():
    print(f'Год {year}:')
    for m in months:
        if m in months:
            print(f'{m}: {months[m]}')


# task.3
with open('employees.json', 'r', encoding="utf-8") as jsonfile:
    employees = json.load(jsonfile)

with open('performance.csv', 'r', encoding="utf-8") as csvfile:
    performance = list(csv.DictReader(csvfile))

perf_dict = {
    int(p['employee_id']): int(p['performance'])
    for p in performance
}

employees_2 = []
for emp in employees:
    emp['производительность'] = perf_dict.get(emp['id'])
    employees_2.append(emp)

avg_perf = sum(perf_dict.values()) / len(perf_dict)
max_id = max(perf_dict, key=perf_dict.get)
for emp in employees_2:
    if emp['id'] == max_id:
        max_name = emp['имя']
        break

print('\n3. JSON & CSV')
print('Средняя производительность:', avg_perf)
print('Сотрудника с наивысшей производительностью:', max_name)
