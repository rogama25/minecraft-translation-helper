import getpass
import sys
import easygui
import os

firstFileLines = []
isTranslationLine = []
firstFileKeys = []
firstFileTranslations = {}
secondFileTranslations = {}
commonKeys = []
firstFileURI = None
secondFileURI = None

def print_welcome_message():
    print("""
Welcome to my Minecraft translation helper.

You can find the source code, along with the license and the changelog at https://github.com/rogama25/minecraft-translation-helper

I would also appreciate it if you contribute to the project, reporting issues or (in the future), donating.

Press Enter to continue.""")
    getpass.getpass(prompt='')

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

def print_translation_lines(initialLine: int, lines=10):
    finalLine = initialLine+10
    if len(commonKeys) < finalLine:
        finalLine = len(commonKeys)
    for i in range(initialLine, finalLine):
        print(str(((i+1)%10)) + ": Untranslated line: " + repr(firstFileTranslations[commonKeys[i]]) + "\n   Translated line: " + repr(secondFileTranslations[commonKeys[i]]) + "\n")

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def open_file(num: int, URI: str = None):
    global firstFileLines, isTranslationLine, firstFileKeys, firstFileTranslations, secondFileTranslations, commonKeys, firstFileURI, secondFileURI
    if URI == None:
        print("Please select the file #" + str(num) + " in the next window. Press Enter to continue.")
        getpass.getpass(prompt='')
    if num == 1:
        firstFileLines = []
        isTranslationLine = []
        firstFileKeys = []
        firstFileTranslations = {}
        if URI == None:
            firstFileURI = easygui.fileopenbox(title="Open file #1",default='*.lang',filetypes=["*.lang"])
            if firstFileURI == None:
                return -1
        else:
            firstFileURI = URI
        with open(firstFileURI,mode='r+') as file:
            for l in file:
                if ("=" not in l) or l.startswith("#"):
                    firstFileLines.append(l)
                    isTranslationLine.append(False)
                else:
                    key,value = l.split("=",1)
                    firstFileLines.append(key)
                    isTranslationLine.append(True)
                    firstFileKeys.append(key)
                    if value.endswith("\n"):
                        value = value[:-1]
                    firstFileTranslations[key] = value
    elif num == 2:
        line = 0
        secondFileTranslations = {}
        if URI == None:
            secondFileURI = easygui.fileopenbox(title="Open file #2",default='*.lang',filetypes=["*.lang"])
            if secondFileURI == None:
                return -1
        else:
            secondFileURI = URI
        with open(secondFileURI,mode='r+') as file:
            for l in file:
                if ("=" in l) and not l.startswith("#"):
                    key,value = l.split("=",1)
                    if value.endswith("\n"):
                        value = value[:-1]
                    secondFileTranslations[key] = value
                    recalculate_common()
    else:
        return -1

def add_untranslated():
    global firstFileLines, isTranslationLine, firstFileKeys, firstFileTranslations, secondFileTranslations, commonKeys, firstFileURI, secondFileURI
    for key in firstFileKeys:
        if key not in secondFileTranslations:
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
    global firstFileLines, isTranslationLine, firstFileKeys, firstFileTranslations, secondFileTranslations, commonKeys, firstFileURI, secondFileURI
    cls()
    print("You are now translating " + key + "\n")
    print("Unstranslated line: " + repr(firstFileTranslations[key]) +"\n")
    if key in secondFileTranslations:
        print("Current translated line: " + repr(secondFileTranslations[key]) + "\n")
    print("Type the new translation:")
    i = input()
    secondFileTranslations[key] = i
    recalculate_common()

def save():
    global firstFileLines, isTranslationLine, firstFileKeys, firstFileTranslations, secondFileTranslations, commonKeys, firstFileURI, secondFileURI
    l = 0
    with open(secondFileURI, "w+") as file:
        for line in firstFileLines:
            if isTranslationLine[l] == True:
                if line in secondFileTranslations:
                    file.write(line + "=" + secondFileTranslations[line] + "\n")
            else:
                file.write(line)
            l += 1

def recalculate_common():
    global firstFileLines, isTranslationLine, firstFileKeys, firstFileTranslations, secondFileTranslations, commonKeys, firstFileURI, secondFileURI
    commonKeys = []
    for key in firstFileKeys:
        if key in secondFileTranslations:
            commonKeys.append(key)

def main():
    global firstFileLines, isTranslationLine, firstFileKeys, firstFileTranslations, secondFileTranslations, commonKeys, firstFileURI, secondFileURI
    print_welcome_message()
    isOpenFile1 = False
    isOpenFile2 = False
    currentTranslationIndex = 0
    while True:
        if isOpenFile1 != True:
            if open_file(1) != -1:
                isOpenFile1 = True
            else:
                continue
        if isOpenFile2 != True:
            if open_file(2) != -1:
                isOpenFile2 = True
            else:
                continue
        cls()
        show_main_help()
        print_translation_lines(currentTranslationIndex)
        option = input()
        if option.lower() == 'u':
            add_untranslated()
        elif option.lower() == 'n':
            if currentTranslationIndex + 10 < len(commonKeys):
                currentTranslationIndex += 10
            else:
                print("Not enough lines to show next page. Press Enter.")
                getpass.getpass(prompt='')
        elif option.lower() == 'p':
            if currentTranslationIndex > 0:
                currentTranslationIndex -= 10
            else:
                print("Not enough lines to show previous page. Press Enter.")
                getpass.getpass(prompt='')
        elif option.lower() == 'a':
            show_about()
        elif option.lower() == 'c':
            isOpenFile1 = False
            isOpenFile2 = False
            currentTranslationIndex = 0
        elif option.lower() == 's':
            save()
        elif option.lower() == 'r':
            open_file(1,firstFileURI)
            open_file(2,secondFileURI)
        elif option.lower() == 'e':
            print("Exit? Any unsaved changes will be lost. [Y to exit]")
            i = input()
            if i.lower() == 'y':
                sys.exit()
        elif option == '':
            pass
        else:
            try:
                option = int(option)
                if option >= 0 and option <=9:
                    if option == 0:
                        option = 9
                    else:
                        option -= 1
                    edit(commonKeys[currentTranslationIndex+option])
                else:
                    raise ValueError()
            except ValueError:
                print("Please input a valid character.")
                getpass.getpass(prompt='')

if __name__ == "__main__":
    main()
