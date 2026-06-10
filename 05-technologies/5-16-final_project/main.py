import json
import csv

# 1
print('task.1')
with open('student_list.json', 'r', encoding="utf-8") as jsonfile:
    students = json.load(jsonfile)

def get_avarage_score(data):
    return sum(data.values()) / len(data)

students_avarage_score = {}

for i, v in students.items():
    students_avarage_score[i] = get_avarage_score(v['grades'])
    print(f'Средний бал для студента {i}:', get_avarage_score(v['grades']))

# 2
print('\nTask.2')

def get_best_student(data):
    return max(data.items(), key=lambda x: x[1])

def get_worst_student(data):
    return min(data.items(), key=lambda x: x[1])

best_student = get_best_student(students_avarage_score)
print('Налучший студент:', best_student[0], f'(Средний балл: {best_student[1]})')

worst_student = get_worst_student(students_avarage_score)
print('Худший студент:', worst_student[0], f'(Средний балл: {worst_student[1]})')

# 3
print('\nTask.3')

def find_student(name):
    try:
        student = students[name]
        print('Имя:', name)
        print('Возраст:', student['age'])
        print('Предметы:', student['subjects'])
        print('Оценки:', student['grades'])
    except Exception as e:
        print('Студент с таким именем не найден')

find_student('John')
print()
find_student('Eva')

# 4
print('\nTask.4')
sorted_student = sorted(students_avarage_score.items(), key=lambda x: x[1], reverse=True)
print('Сортировка студентов по среднему баллу:')
for i, v in sorted_student:
    print(f'{i}: {v}')

# 5
print('\nTask.5')

def add_mame(x, y):
    return dict({'name': y}, **x)

students = list(map(lambda x: add_mame(x[1], x[0]), students.items()))
print(students)

# 6
print('\nTask.6')
data = list(map(lambda x: {'name': x['name'], 'age': x['age'], 'grade': get_avarage_score(x['grades'])}, students))
with open('students.csv', 'w', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'age', 'grade']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(data)