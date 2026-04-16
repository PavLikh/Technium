import itertools

# 1
print('1.Комбинация чисел')
l = [1, 2, 3, 4]
for c in itertools.combinations(l, 2):
    print(c)

# 2
s = 'Python'
print('\n2.Перебор перестановок букв в слове')
for p in itertools.permutations(s):
    print(''.join(p))

# 3
print('\n3.Объединение списков в цикле')
CYCLE = 5
list1 = ['a', 'b']
list2 = [1, 2, 3]
list3 = ['x', 'y']
list_res = []

l1 = list(itertools.chain(list1, list2, list3))
max_len = len(l1)
for item in itertools.islice(itertools.cycle(l1), max_len * CYCLE):
    list_res.append(item)
print(list_res)

# 4
print('\n4.Генерация бесконечной последовательности чисел')
COUNT_10 = 10
def generate_fibonacci():
    prev_prev, prev = 0, 1
    while True:
        yield prev_prev
        prev_prev, prev = prev, prev_prev + prev

for num in itertools.islice(generate_fibonacci(), COUNT_10):
    print(num, end = ' ')
print()

# 5
print('\n5: Составление всех возможных комбинаций слов')
l1 = ['red', 'blue']
l2 = ['shirt', 'shoes']
for i in itertools.product(l1,l2):
    print(i)
