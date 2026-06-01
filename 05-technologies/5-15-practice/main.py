# 1
students_dict = {'Саша': 27, 'Кирилл': 52, 'Маша': 14, 'Петя': 36, 'Оля': 43, }
sorted_dict = sorted(students_dict.items(), key=lambda x: x[1])
print(sorted_dict)

#2
data = [
    (82, 191),
    (68, 184),
    (90, 189),
    (73, 179),
    (76, 184),
    (82, 180)
]
sorted_in = sorted(data, key=lambda x: x[0] / (x[1] * x[1]))
print(sorted_in)

#3
students_list = [
    {
        "name": "Саша",
        "age": 27,
    },
    {
        "name": "Кирилл",
        "age": 52,
    },
    {
        "name": "Маша",
        "age": 14,
    },
    {
        "name": "Петя",
        "age": 36,
    },
    {
        "name": "Оля",
        "age": 43,
    }
]
youngest = min(students_list, key=lambda x: x["age"])
print(youngest)