import random

def generate_sets():
    sets = []
    for _ in range(20):
        # Генерируем 3 уникальных числа в диапазоне от 1 до 18
        numbers = random.sample(range(1, 19), 3)
        sets.append(numbers)
    return sets

# Генерируем 20 наборов
sets = generate_sets()

# Выводим результат
for i, s in enumerate(sets, 1):
    s.sort()
    print(f"- Студент {i}: лекции {s}")
