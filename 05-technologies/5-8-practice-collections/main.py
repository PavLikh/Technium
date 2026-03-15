import random

from collections import namedtuple
from collections import Counter
from collections import deque
from collections import defaultdict

# 1.
x = random.randrange(10, 30)
l = [random.randint(1, 20) for _ in range(x)]
print('1.Список:', l)
counter = Counter(l)
most_common = counter.most_common(3)
for num, quant in most_common:
    print('Элемент', num, '-',quant)

# 2.
Book = namedtuple('Book', ['title', 'author', 'genre'])
print('\n2.Работа с имнованными кортежами')

data = [
    ('The Iliad', 'Homer', 'Epic'),
    ('War and peace', 'L.N.Tolstoi', 'Novel'),
    ('Hamlet', 'Shakespeare', 'Drama')
]

books = [Book(*row) for row in data]
for b in books:
    print('Tittle:', b.title, 'Author:', b.author, 'Genre:', b.genre)

# 3.
print('\n3.Работа с defaultdict')
d = defaultdict(list)
d['a'].append(1)
d['a'].append(2)
d['a'].append(3)
d['b'].append('hello')
d['b'].append('world')
for key, val in d.items():
    print(key, val)

# 4.
print('\n4.Использование deque')
queue = deque(['el1','el2'])
print(queue)
queue.append('end')
print('Append:', queue)  # Вывод: deque([0, 1, 2, 3, 4])
queue.appendleft('start')  # Добавление элемента в начало
print('appendleft:',queue)  # Вывод: deque([0, 1, 2, 3, 4])
queue.pop()
print('Pop:',queue)
queue.popleft()
print('Popleft',queue)

# 5.
print('\n5.Простая очередь deque')
class Queue:
    def __init__(self):
        self.items = deque()

    def __getitem__(self, index):
        return self.items[index]

    def __iter__(self):
        return iter(self.items)
    
    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)
    
    def push(self, item):
        self.items.appendleft(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.popleft()
        else:
            raise IndexError("Queue is empty")

    def rem_last(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Queue is empty")

    def size(self):
        return len(self.items)
    
    def show_in_line(self) -> None:
        for key, val in enumerate(queue):
            print(key, '-', val, end =' | ')
        print()

queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
queue.show_in_line()
queue.push(11)
queue.push(10)
queue.show_in_line()
queue.rem_last()
queue.show_in_line()
queue.dequeue()
queue.show_in_line()
