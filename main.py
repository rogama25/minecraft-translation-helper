import getpass
import sys
import easygui
import os


def print_welcome_message():
    print("""
Welcome to my Minecraft translation helper.

You can find the source code, along with the license and the changelog at https://github.com/rogama25/minecraft-translation-helper

I would also appreciate it if you contribute to the project, reporting issues or (in the future), donating.

Press Enter to continue.""")
    getpass.getpass(prompt='')

def showMainHelp():
    print("""Welcome to the main screen. You can press the following keys:
U: Add missing translations.
N: Show the next set of lines.
P: Show previous lines.
A: Show the about page.
C: Close the translation files.
S: Save changes.
Or press a number to edit its line.""")

def printTranslationLines(initialLine: int, lines=10):
    global firstFileTranslations, commonKeys, secondFileTranslations
    finalLine = initialLine+10
    if len(commonKeys) < finalLine:
        finalLine = len(commonKeys)
    for i in range(initialLine, finalLine):
        print(str(((i+1)%10)) + ": Untranslated line: " + firstFileTranslations[commonKeys[i]] + "\n   Translated line: " + secondFileTranslations[commonKeys[i]] + "\n")

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def openFile(num: int):
    global firstFileLines, isTranslationLane, firstFileTranslations, firstFileKeys, firstFileURI, secondFileTranslations, secondFileURI, commonKeys
    print("Please select the file #" + str(num) + " in the next window. Press Enter to continue.")
    getpass.getpass(prompt='')
    if num == 1:
        line = 0
        firstFileLines = []
        isTranslationLine = []
        firstFileKeys = []
        firstFileTranslations = {}
        firstFileURI = easygui.fileopenbox(title="Open file #1",default='*.lang',filetypes=["*.lang"])
        if firstFileURI == None:
            return -1
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
                line += 1
        print(str(firstFileTranslations) + "\n\n\n")
    elif num == 2:
        line = 0
        secondFileTranslations = {}
        secondFileURI = easygui.fileopenbox(title="Open file #2",default='*.lang',filetypes=["*.lang"])
        if secondFileURI == None:
            return -1
        with open(secondFileURI,mode='r+') as file:
            for l in file:
                if ("=" in l) and not l.startswith("#"):
                    key,value = l.split("=",1)
                    if value.endswith("\n"):
                        value = value[:-1]
                    secondFileTranslations[key] = value
                line += 1
        print(str(secondFileTranslations) + "\n\n\n")
        commonKeys = []
        for key in firstFileKeys:
            if key in secondFileTranslations:
                commonKeys.append(key)
        print(commonKeys)
    else:
        return -1

def main():
    print_welcome_message()
    isOpenFile1 = False
    isOpenFile2 = False
    currentTranslationIndex = 0
    while True:
        if isOpenFile1 != True:
            if openFile(1) != -1:
                isOpenFile1 = True
            else:
                continue
        if isOpenFile2 != True:
            if openFile(2) != -1:
                isOpenFile2 = True
            else:
                continue
        cls()
        showMainHelp()
        printTranslationLines(currentTranslationIndex)
        input()

if __name__ == "__main__":
    main()
