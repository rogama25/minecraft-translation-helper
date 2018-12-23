import getpass
import sys
import easygui


def print_welcome_message():
    print("""
Welcome to my Minecraft translation helper.

You can find the source code, along with the license and the changelog at https://github.com/rogama25/minecraft-translation-helper

I would also appreciate it if you contribute to the project, reporting issues or (in the future), donating.

Press Enter to continue.""")
    getpass.getpass(prompt='')

def openFile(num: int):
    print("Please select the file #" + str(num) + " in the next window. Press Enter to continue.")
    getpass.getpass(prompt='')
    if num == 1:
        line = 0
        global firstFileLines, isTranslationLane, firstFileTranslations, firstFileKeys, firstFileURI
        firstFileLines = []
        isTranslationLane = []
        firstFileKeys = []
        firstFileTranslations = {}
        firstFileURI = easygui.fileopenbox(title="Open file #1",default='*.lang',filetypes=["*.lang"])
        if firstFileURI == None:
            return -1
        with open(firstFileURI,mode='r+') as file:
            for l in file:
                if ("=" not in l) or l.startswith("#"):
                    firstFileLines.append(l)
                    isTranslationLane.append(False)
                else:
                    key,value = l.split("=",1)
                    firstFileLines.append(key)
                    isTranslationLane.append(True)
                    firstFileKeys.append(key)
                    if value.endswith("\n"):
                        value = value[:-1]
                    firstFileTranslations[key] = value
                line += 1
            print(str(firstFileTranslations) + "\n\n\n")
    elif num == 2:
        line = 0
        global secondFileTranslations, secondFileURI
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
            print(secondFileTranslations)
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


if __name__ == "__main__":
    main()
