# 1
strings = ["apple", "kiwi", "banana", "fig"]
filtered_stings = list(filter(lambda x: len(x) > 4, strings))
print(filtered_stings)

# 2
students = [{"name": "John", "grade": 90}, {"name": "Jane", "grade": 85}, {"name": "Dave", "grade": 92}]
max_grade_students = max(students, key=lambda student: student['grade'])
print(max_grade_students)

# 3
l = [(1, 5), (3, 2), (2, 8), (4, 3)]
sorted_l = sorted(l, key=lambda x: sum(x))
print(sorted_l)

#4
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers) # Вывод [2, 4, 6, 8, 10]

#5
class Person:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
    
    def __repr__(self) -> str:
        return f"Student(name='{self.name}', age='{self.age}')"

persons = [
    Person("John", 19),
    Person("Bill", 21),
    Person("Dave", 30)
]

sorted_persons = sorted(persons, key=lambda x: x.age)
print(sorted_persons)