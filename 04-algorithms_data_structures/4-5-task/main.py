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

brackets = {
    ')':'(',
    ']':'[',
    '}':'{'
}

def check_sequence(s):
    if not s:
        return 'invalid string'
    stack = Stack()
    for char in s:
        if char in brackets.values():
            stack.push(char)
        elif char in brackets.keys():
            if stack.is_empty() or stack.peek() != brackets[char]:
                return  s + ' is wrong sequence'
            stack.pop()
        else:
            return s + ' - invalid string'
    return '\033[92m' + s + ' is valid sequence\033[0m'

strings = [
    "([]{})",
    "([)]",
    "{[}",
    "()"
]

for s in strings:
    print(check_sequence(s))
