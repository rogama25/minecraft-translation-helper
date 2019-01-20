import getpass
import sys
import easygui
import os

first_file_lines = []
is_translation_line = []
first_file_keys = []
first_file_translations = {}
second_file_translations = {}
common_keys = []
first_file_uri = None
second_file_uri = None


def press_enter():
	getpass.getpass(prompt='')


def print_welcome_message():
	print("""
Welcome to my Minecraft translation helper.

You can find the source code, along with the license and the changelog at https://github.com/rogama25/minecraft-translation-helper

I would also appreciate it if you contribute to the project, reporting issues or (in the future), donating.

Press Enter to continue.""")
	press_enter()


def show_main_help():
	print("""Welcome to the main screen. You can press the following keys:
U: Add missing translations.
N: Show the next set of lines.
P: Show previous lines.
A: Show the about page.
C: Close the translation files.
S: Save changes to disk.
R: Reload lines from disk.
E: Exit.
Or press a number to edit its line.
""")


def print_translation_lines(initial_line: int, lines=10):
	final_line = initial_line + lines
	if len(common_keys) < final_line:
		final_line = len(common_keys)
	for i in range(initial_line, final_line):
		print(str(((i + 1) % lines)) + ": Untranslated line: " + repr(
			first_file_translations[common_keys[i]]) + "\n   Translated line: " + repr(
			second_file_translations[common_keys[i]]) + "\n")


def cls():
	os.system('cls' if os.name == 'nt' else 'clear')


def open_file(num: int, uri: str = None):
	global first_file_lines, is_translation_line, first_file_keys, first_file_translations, second_file_translations, common_keys, first_file_uri, second_file_uri
	if uri is None:
		print("Please select the file #" + str(num) + " in the next window. Press Enter to continue.")
		press_enter()
	if num == 1:
		first_file_lines = []
		is_translation_line = []
		first_file_keys = []
		first_file_translations = {}
		if uri is None:
			first_file_uri = easygui.fileopenbox(title="Open file #1", default='*.lang', filetypes=["*.lang"])
			if first_file_uri is None:
				return -1
		else:
			first_file_uri = uri
		with open(first_file_uri, mode='r+', encoding="utf-8") as file:
			for l in file:
				if ("=" not in l) or l.startswith("#"):
					first_file_lines.append(l)
					is_translation_line.append(False)
				else:
					key, value = l.split("=", 1)
					first_file_lines.append(key)
					is_translation_line.append(True)
					first_file_keys.append(key)
					if value.endswith("\n"):
						value = value[:-1]
					first_file_translations[key] = value
	elif num == 2:
		second_file_translations = {}
		if uri is None:
			second_file_uri = easygui.fileopenbox(title="Open file #2", default='*.lang', filetypes=["*.lang"])
			if second_file_uri is None:
				return -1
		else:
			second_file_uri = uri
		with open(second_file_uri, mode='r+', encoding="utf-8") as file:
			for l in file:
				if ("=" in l) and not l.startswith("#"):
					key, value = l.split("=", 1)
					if value.endswith("\n"):
						value = value[:-1]
					second_file_translations[key] = value
					recalculate_common()
	else:
		return -1


def add_untranslated():
	global first_file_lines, is_translation_line, first_file_keys, first_file_translations, second_file_translations, common_keys, first_file_uri, second_file_uri
	for key in first_file_keys:
		if key not in second_file_translations:
			edit(key)
			print("Return to main menu? Type y to exit, anything else to translate next line.")
			i = input()
			if i.lower() == 'y':
				return


def show_about():
	cls()
	print("""Software created by rogama25.

Source code available at: https://github.com/rogama25/minecraft-translation-helper

Distributed under the GNU GPLv3

Version 0.1

Press Enter to return to main menu.""")
	getpass.getpass(prompt='')


def edit(key: str):
	global first_file_lines, is_translation_line, first_file_keys, first_file_translations, second_file_translations, common_keys, first_file_uri, second_file_uri
	cls()
	print("You are now translating " + key + "\n")
	print("Untranslated line: " + repr(first_file_translations[key]) + "\n")
	if key in second_file_translations:
		print("Current translated line: " + repr(second_file_translations[key]) + "\n")
	print("Type the new translation:")
	i = input()
	second_file_translations[key] = i
	recalculate_common()


def save():
	global first_file_lines, is_translation_line, first_file_keys, first_file_translations, second_file_translations, common_keys, first_file_uri, second_file_uri
	line_number = 0
	with open(second_file_uri, "w+", encoding="utf-8") as file:
		for line in first_file_lines:
			if is_translation_line[line_number]:
				if line in second_file_translations:
					file.write(line + "=" + second_file_translations[line] + "\n")
			else:
				file.write(line)
			line_number += 1


def recalculate_common():
	global first_file_lines, is_translation_line, first_file_keys, first_file_translations, second_file_translations, common_keys, first_file_uri, second_file_uri
	common_keys = []
	for key in first_file_keys:
		if key in second_file_translations:
			common_keys.append(key)


def main():
	global first_file_lines, is_translation_line, first_file_keys, first_file_translations, second_file_translations, common_keys, first_file_uri, second_file_uri
	print_welcome_message()
	is_open_file1 = False
	is_open_file2 = False
	current_translation_index = 0
	while True:
		if not is_open_file1:
			if open_file(1) != -1:
				is_open_file1 = True
			else:
				continue
		if not is_open_file2:
			if open_file(2) != -1:
				is_open_file2 = True
			else:
				continue
		cls()
		show_main_help()
		print_translation_lines(current_translation_index)
		option = input()
		if option.lower() == 'u':
			add_untranslated()
		elif option.lower() == 'n':
			if current_translation_index + 10 < len(common_keys):
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
			save()
		elif option.lower() == 'r':
			open_file(1, first_file_uri)
			open_file(2, second_file_uri)
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
					edit(common_keys[current_translation_index + option])
				else:
					raise ValueError()
			except ValueError:
				print("Please input a valid character.")
				press_enter()


if __name__ == "__main__":
	main()
