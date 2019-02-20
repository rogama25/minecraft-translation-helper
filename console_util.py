import getpass
import os


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
