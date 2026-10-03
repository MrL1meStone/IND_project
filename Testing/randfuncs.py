from random import randint

def randstr():
	return "".join([chr(randint(65,91)) for i in range(randint(1,12))])

