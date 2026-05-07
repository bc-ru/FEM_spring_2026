import random

# Создаем список чисел от 1 до 20
numbers = list(range(1, 21))

# Перемешиваем список случайным образом
random.shuffle(numbers)

# Разбиваем список на 4 группы по 5 чисел
groups = [numbers[i:i + 5] for i in range(0, len(numbers), 5)]

# Выводим результат
for i, group in enumerate(groups, start=1):
    print(f"Проект {i}: {group}")
