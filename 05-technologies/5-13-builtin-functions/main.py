from functools import reduce

# 1 cube
def cube(x):
    return x * x * x

numbers = [1, 2, 3, 4, 5]
squared = list(map(cube, numbers))
print(squared)

# 4 multiple_of_five
def multiple_of_five(x):
    return x % 5 == 0

numbers = [1, 20, 31, 45, 50]
multiple_of_five_numbers = list(filter(multiple_of_five, numbers))
print(multiple_of_five_numbers)


def is_even(x):
    return x % 2 == 0
# 3
def odd(x):
    return x % 2 != 0

numbers = [1, 2, 3, 4, 5, 6, 7]
odd_numbers = list(filter(odd, numbers))

def multiply(x, y):
    return x * y

product = reduce(multiply, odd_numbers)
print(product)
