# 1.Алгоритм проверки наличия дубликатов в массиве.
def has_duplicates(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False

arr = [1, 2, 3, 4, 5, 6, 7, 100, 100, 150, 200]     
print('1.Есть ли дубликаты:', has_duplicates(arr), 'сложность O(n^2)')

# 2.Алгоритм поиска максимального элемента в неотсортированном массиве.
def find_max(arr):
    max_val = arr[0]
    for val in arr:
        if val > max_val:
            max_val = val
    return max_val

arr = [100, 2, 5, 7, 6, 3, 1, 100, 150, 200, 4]
print('2.Поиска максимального элемента:', find_max(arr), 'сложность O(n)')

# 3.Алгоритм сортировки выбором (Selection Sort).
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
arr = [100, 2, 5, 7, 6, 3, 1, 150, 200, 4]
selection_sort(arr)
print('3.Selection Sort:', arr, 'сложность O(n^2)')

# 4.Алгоритм быстрой сортировки (Quick Sort).
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
arr = [100, 2, 5, 7, 6, 3, 1, 150, 200, 4]
selection_sort(arr)
print('4.Quick Sort:', arr, 'сложность O(n(logn) либо O(n^2)')

# 5.Алгоритм вычисления n-го числа Фибоначчи (рекурсивно).
def fibonacci_recursive(n):
    print(n)
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
print('5.fibonacci:', fibonacci_recursive(7), 'сложность O(2^n)')
