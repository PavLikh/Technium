import csv

# Задание.1
with open('prices.txt') as f:
    s = f.read()
    l = s.split('   ')

data = []
for item in l:
    data.append(item.split(','))

header = data[0]

with open('prices.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)  # Записываем данные в файл

csvfile.close()

# Задание.2
with open('prices.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    price = 0
    for row in reader:
        price += int(row[header[1]]) * int(row[header[2]])

print('Общая сумма:', price)
