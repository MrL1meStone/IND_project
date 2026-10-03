import sys
import io
import traceback
import importlib
from contextlib import redirect_stdout


def check_output(input_func, output_func) -> tuple[bool, str]:
	try:
		from Testing import temporary
		importlib.reload(temporary)
	except BaseException:
		error = traceback.format_exc()
		error = error.split('temporary.py", ')[-1]
		return False, error

	original_stdin = sys.stdin
	sys_stdout = sys.stdout
	is_right_output=[]

	for _ in range(5):
		input_data = input_func()
		f = io.StringIO()

		with redirect_stdout(f):
			sys.stdin = io.StringIO("\n".join(input_data.values()))
			try:
				temporary.temporary()
				out = f.getvalue()
				is_right_output.append(out.strip() == output_func(**input_data))

			except BaseException:
				sys.stdout = sys_stdout
				sys.stdin = original_stdin
				error = traceback.format_exc()
				error = error.split('temporary.py", ')[-1]
				return False, error

	sys.stdout = sys_stdout
	sys.stdin = original_stdin
	return all(is_right_output), ""
