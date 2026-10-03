from os.path import exists

def make_module(text: str):
	if exists('Testing/temporary.py'):
		mode = "w"
	else:
		mode = "a"

	text = text.split("\n")

	with open('Testing/temporary.py', mode) as module:
		module.write('def temporary():\n')

		for line in text:
			module.write(f'    {line}\n')
		module.write('    pass')