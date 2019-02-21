import getpass
import os
from Translations import Translations
import easygui


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


def cls():
	os.system('cls' if os.name == 'nt' else 'clear')


def show_about():
	cls()
	print("""Software created by rogama25.

Source code available at: https://github.com/rogama25/minecraft-translation-helper

Distributed under the GNU GPLv3

Version 0.1

Press Enter to return to main menu.""")
	getpass.getpass(prompt='')


def edit(tr: Translations, key: str):
	cls()
	print("You are now translating " + key + "\n")
	print("Untranslated line: " + repr(tr.first_file_translations[key]) + "\n")
	if key in tr.second_file_translations:
		print("Current translated line: " + repr(tr.second_file_translations[key]) + "\n")
	print("Type the new translation:")
	i = input()
	tr.second_file_translations[key] = i
	tr.recalculate_common()


def add_untranslated(tr: Translations):
	for key in tr.first_file_keys:
		if key not in tr.second_file_translations:
			edit(tr, key)
			print("Return to main menu? Type y to exit, anything else to translate next line.")
			i = input()
			if i.lower() == 'y':
				return


def print_translation_lines(tr: Translations, initial_line: int, lines=10):
	final_line = initial_line + lines
	if len(tr.common_keys) < final_line:
		final_line = len(tr.common_keys)
	for i in range(initial_line, final_line):
		print(str(((i + 1) % lines)) + ": Untranslated line: " + repr(
			tr.first_file_translations[tr.common_keys[i]]) + "\n   Translated line: " + repr(
			tr.second_file_translations[tr.common_keys[i]]) + "\n")


def open_file(tr: Translations, num: int, uri: str = None):
	if uri is None:
		print("Please select the file #" + str(num) + " in the next window. Press Enter to continue.")
		press_enter()
		uri = easygui.fileopenbox(title="Open file #" + str(num), default='*.lang', filetypes=["*.lang"])
	if uri is None:
		return -1
	if num == 1:
		tr.first_file_uri = uri
		tr.load_first()
	elif num == 2:
		tr.second_file_uri = uri
		tr.load_second()
