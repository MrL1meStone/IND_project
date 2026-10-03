from random import randint, choice
from Testing.randfuncs import randstr

hard_questions = [
	{
		"text": "Введите строку и выведите самый часто встречающийся символ.",
		"func": lambda a: max(set(a), key=a.count),
		"args": lambda: {'a': randstr()}
	},
	{
		"text": "Введите несколько чисел через пробел и найдите второе по величине число.",
		"func": lambda lst: str(sorted(set(map(int, lst.split())))[-2]),
		"args": lambda: {'lst': " ".join(str(randint(1, 50)) for _ in range(6))}
	},
	{
		"text": "Введите строку и проверьте, является ли она изограммой (без повторяющихся букв).",
		"func": lambda a: str(len(set(a.lower())) == len(a)),
		"args": lambda: {'a': choice(["lamp", "hello", "world", "python"])}
	},
	{
		"text": "Введите строку и выведите все символы, которые встречаются более одного раза.",
		"func": lambda a: str([ch for ch in set(a) if a.count(ch) > 1]),
		"args": lambda: {'a': randstr()}
	},
	{
		"text": "Введите несколько чисел через пробел и проверьте, является ли последовательность возрастающей.",
		"func": lambda lst: str(all(x < y for x, y in zip(map(int, lst.split()), map(int, lst.split())[1:]))),
		"args": lambda: {'lst': " ".join(str(randint(1, 20)) for _ in range(5))}
	},
	{
		"text": "Введите число и выведите список всех его делителей.",
		"func": lambda a: str([i for i in range(1, a + 1) if a % i == 0]),
		"args": lambda: {'a': randint(10, 50)}
	},
	{
		"text": "Введите строку и подсчитайте количество слов, начинающихся с гласной.",
		"func": lambda a: str(sum(word[0].lower() in "aeiouаеёиоуыэюя" for word in a.split())),
		"args": lambda: {'a': " ".join(randstr() for _ in range(6))}
	},
	{
		"text": "Введите несколько чисел через пробел и найдите длину самой длинной серии одинаковых чисел.",
		"func": lambda lst: str(max(len(list(g)) for _, g in __import__('itertools').groupby(lst.split()))),
		"args": lambda: {'lst': " ".join(str(choice([1,2,3])) for _ in range(10))}
	},
	{
		"text": "Введите строку и выведите её в виде 'a1b2c3' (символ + его позиция).",
		"func": lambda a: str("".join(f"{ch}{i+1}" for i, ch in enumerate(a))),
		"args": lambda: {'a': randstr()}
	},
	{
		"text": "Введите несколько чисел через пробел и проверьте, можно ли из них составить арифметическую прогрессию.",
		"func": lambda lst: str(len(set(b - a for a, b in zip(sorted(map(int, lst.split())), sorted(map(int, lst.split()))[1:]))) == 1),
		"args": lambda: {'lst': " ".join(str(randint(1, 20)) for _ in range(5))}
	}
]
