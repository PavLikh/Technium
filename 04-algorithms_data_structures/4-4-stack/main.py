class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Стек пуст")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Стек пуст")

    def size(self):
        return len(self.items)

# Создаем экземпляр стека
my_stack = Stack()

# Добавляем элементы в стек
my_stack.push(5)
my_stack.push(10)
my_stack.push(15)

# Просматриваем вершину стека
print("Вершина стека:", my_stack.peek())

# Удаляем элемент из стека
my_stack.pop()

# Проверяем, пуст ли стек
print("Стек пуст?", my_stack.is_empty())

# Выводим размер стека
print("Размер стека:", my_stack.size())
