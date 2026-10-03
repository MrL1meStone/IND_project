from random import randint, choice
from Testing.randfuncs import randstr

normal_questions = [
	{
		"text": 'Введите число и выведите "да" если четное, "нет" иначе',
		"func": lambda a: 'да' if int(a) % 2 == 0 else 'нет',
		"args": lambda: {'a': str(randint(1, 1000))}
	},
	{
		"text": "Введите несколько чисел через пробел и найдите их сумму.",
		"func": lambda lst: str(sum(list(map(int, lst.split(" "))))),
		"args": lambda: {'lst': " ".join([str(randint(-50, 50)) for _ in range(randint(3, 10))])}
	},
	{
		"text": "Введите строку и узнайте, сколько в ней гласных букв.",
		"func": lambda a: str(sum(ch.lower() in "aeiouаеёиоуыэюя" for ch in a)),
		"args": lambda: {'a': randstr()}
	},
	{
		"text": "Введите строку и проверьте, является ли она палиндромом.",
		"func": lambda a: str(a.lower().replace(" ", "") == a.lower().replace(" ", "")[::-1]),
		"args": lambda: {'a': choice(["казак", "дом", "шалаш", "python", "madam"])}
	},
	{
		"text": "Введите несколько чисел через пробел и выведите их квадраты.",
		"func": lambda lst: str([i**2 for i in list(map(int, lst.split()))]),
		"args": lambda: {'lst': " ".join([str(randint(1, 10)) for _ in range(randint(3, 8))])}
	},
	{
		"text": "Введите строку и замените все цифры символом *.",
		"func": lambda a: str("".join("*" if ch.isdigit() else ch for ch in a)),
		"args": lambda: {'a': "".join(choice("abc123xyz") for _ in range(randint(5, 12)))}
	},
	{
		"text": "Введите несколько слов и выведите те, длина которых больше 3 символов.",
		"func": lambda a: str([word for word in a.split() if len(word) > 3]),
		"args": lambda: {'a': " ".join([randstr(randint(2, 6)) for _ in range(randint(4, 8))])}
	},
	{
		"text": "Введите строку и выведите, сколько раз встречается каждый символ.",
		"func": lambda a: str({ch: a.count(ch) for ch in a}),
		"args": lambda: {'a': randstr()}
	},
	{
		"text": "Введите список слов и удалите из него дубликаты.",
		"func": lambda lst: str(list(dict.fromkeys(lst.split()))),
		"args": lambda: {'lst': " ".join([choice(["apple", "banana", "apple", "pear", "banana", "kiwi"]) for _ in range(randint(5, 8))])}
	},
	{
		"text": "Введите два числа: проверьте, входит ли первое в диапазон от 0 до второго.",
		"func": lambda a,b: str(a in range(0, b + 1)),
		"args": lambda: {'a': randint(0, 10), 'b': randint(5, 15)}
	}
]
