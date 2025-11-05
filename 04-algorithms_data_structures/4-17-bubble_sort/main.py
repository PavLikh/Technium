def bubble_sort(arr):
    length = len(arr)
    for i in range(length - 1):
        for j in range(length - 1 - i):
            if arr[j] > arr[j+1]:
                buff = arr[j]
                arr[j] = arr[j+1] 
                arr[j+1] = buff


# Пример использования:
my_list = [64, 34, 25, 12, 22, 11, 90]
bubble_sort(my_list)
print("Отсортированный список:", my_list)