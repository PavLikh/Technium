def insertion_sort(arr):
    length = len(arr)
    for i  in range(length - 1):
        x = arr[i + 1]
        j = i + 1
        while j > 0 and arr[j - 1] > x:
            arr[j] = arr[j - 1]
            j -= 1
        arr[j] = x

# Пример использования:
my_list = [64, 34, 25, 12, 22, 11, 90]
insertion_sort(my_list)
print("Отсортированный список:", my_list)