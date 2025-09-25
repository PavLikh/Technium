from operator import add, sub, mul, truediv, floordiv, mod, pow

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

    def clear(self):
        self.items.clear()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Стек пуст")

    def size(self):
        return len(self.items)

ops = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '//': floordiv,
    '%': mod,
    '**': pow
}

stack = Stack()

def calculate(l):
    for val in l:
        if val.isdigit():
            stack.push(float(val))
        elif val in ops.keys():
            if stack.size() > 1:
                b = stack.pop()
                a = stack.pop()
                calcul = ops[val](a, b)
                stack.push(float(calcul))
            else:
                stack.clear()
                raise ValueError("Wrong expression")
    stack.clear()
    return calcul

strings = [
    '3 2 1 // +',
    "3 4 2 * + +",
    "2 10 5 / *",
    "100 5 2 2 ** * /"
]

for s in strings:
    l = s.split()
    try:
        print(calculate(l))
    except Exception as e:
        print('Error:', e)
