import sys
from console_util import *


def main():
	print_welcome_message()
	is_open_file1 = False
	is_open_file2 = False
	tr = Translations()
	current_translation_index = 0
	while True:
		if not is_open_file1:
			if open_file(tr, 1) != -1:
				is_open_file1 = True
			else:
				continue
		if not is_open_file2:
			if open_file(tr, 2) != -1:
				is_open_file2 = True
			else:
				continue
		cls()
		show_main_help()
		print_translation_lines(tr, current_translation_index)
		option = input()
		if option.lower() == 'u':
			add_untranslated(tr)
		elif option.lower() == 'n':
			if current_translation_index + 10 < len(tr.common_keys):
				current_translation_index += 10
			else:
				print("Not enough lines to show next page. Press Enter.")
				press_enter()
		elif option.lower() == 'p':
			if current_translation_index > 0:
				current_translation_index -= 10
			else:
				print("Not enough lines to show previous page. Press Enter.")
				press_enter()
		elif option.lower() == 'a':
			show_about()
		elif option.lower() == 'c':
			is_open_file1 = False
			is_open_file2 = False
			current_translation_index = 0
		elif option.lower() == 's':
			tr.save_second()
		elif option.lower() == 'r':
			tr.load_first()
			tr.load_second()
		elif option.lower() == 'e':
			cls()
			print("Exit? Any unsaved changes will be lost. [Y to exit]")
			i = input()
			if i.lower() == 'y':
				sys.exit()
		elif option == '':
			pass
		else:
			try:
				option = int(option)
				if 0 <= option <= 9:
					if option == 0:
						option = 9
					else:
						option -= 1
					edit(tr, tr.common_keys[current_translation_index + option])
				else:
					raise ValueError()
			except ValueError:
				print("Please input a valid character.")
				press_enter()


if __name__ == "__main__":
	main()
