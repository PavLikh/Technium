def selection_sort(arr):
    length = len(arr)
    for i in range(length - 1):
        min = arr[i]
        index = i
        for j in range(length - 1 - i):
            if arr[j + i] < min:
                min = arr[j + i]
                index = j + i
        if index != i:
            arr[index] = arr[i]
            arr[i] = min



# Пример использования:
my_list = [64, 34, 25, 12, 22, 11, 90]
selection_sort(my_list)
print("Отсортированный список:", my_list)