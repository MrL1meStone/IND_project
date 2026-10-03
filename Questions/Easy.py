from random import randint

from Testing.randfuncs import randstr

easy_questions=[
	{   "text": 'Получите переменную через ввод в консоль и выведите ее',
		"func": lambda a: str(a),
	    "args": lambda: {'a': randstr()}
	},
	{
		"text": 'Получите 2 переменные через консоль и выведите их сумму',
		"func": lambda a,b: str(a+b),
		"args": lambda: {'a': str(randint(1, 10 ** 6)), 'b': str(randint(1, 10 ** 6))}
	},
	{
		"text": 'Получите список строк и выведите список наборов (кортежей) вариантов строк:\n'
		        'Строка с большой буквы, \n'
		        'строка маленькими буквами, \n',
				'СТРОКА БОЛЬШИМИ БУКВАМИ'
		"func": lambda lst: str([(i.capitalize(),i.lower(),i.upper()) for i in lst.split(" ")]),
		"args": lambda: {'lst': " ".join([randstr() for _ in range(randint(1, 20))])}
	},
	{
		"text": 'Получите список в котором на первом месте стоит id,на 2 - name, на 3 - age и\n'
		        'запакуйте с соответствующими ключами в словарь и выведите его',
		"func": lambda lst: str(dict(zip(("id","name","age"),lst.split(" ")))),
		"args": lambda: {"lst": " ".join([str(randint(1,10**12))] + [randstr(),randstr()])}
	},
	{
		"text": 'Выведите кортеж из наименьшего и наибольшего значения списка\n'
				'(элементы подаются в одну строку через пробел)',
		"func": lambda lst: str((min(lst.split(" ")),max(lst.split(" ")))),
		"args": lambda: {'lst': " ".join([str(randint(-5*10**5,5*10**5)) for _ in range(randint(1,5))])}
	},
	{
		"text": 'Выведите сортированный список элементов, находящихся в двух списках,\n'
				'введенных через пробел',
		"func": lambda a,b: str(sorted(list(set(a.split(" ")).intersection(set(b.split(" ")))))),
		"args": lambda: {'a': " ".join([str(randint(-5 * 10 ** 5, 5 * 10 ** 5)) for _ in range(randint(1, 5))]),
		         'b': " ".join([str(randint(-5 * 10 ** 5, 5 * 10 ** 5)) for _ in range(randint(1, 5))])}
	},
	{
		"text": 'Выведите первый и последний элемент списка',
		"func": lambda lst: f"{lst.split(" ")[0]} {lst.split(" ")[-1]}",
		"args": lambda: {'lst': " ".join([str(randint(-5 * 10 ** 5, 5 * 10 ** 5)) for _ in range(randint(1, 5))])}
	},
	{
		"text": 'Выведите сколько раз встречается 2 строка в первой',
		"func": lambda a,b: str(a.count(b)),
		"args": lambda: {'a' : randstr(),'b' : randstr()}
	},
	{
		"text": 'Выведите первое введенное число в степени второго',
		"func": lambda a,b: str(int(a)**int(b)),
		"args": lambda: {'a': str(randint(1,9)),'b': str(randint(4,10))}
	},
	{
		"text": 'Выведите делится ли первое число на второе',
		"func": lambda a,b: str(int(a)%int(b)==0),
		"args": lambda: {'a': str(randint(1,999)),'b': str(randint(1,100))}
	}]