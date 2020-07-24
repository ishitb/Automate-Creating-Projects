import json, colorama, os, sys
from termcolor import colored, cprint
from random import uniform

BASE_PATH = 'C:/Users/Lenovo/Desktop/MyPC/Projects/Miscellaneous/Automate-Creating-Projects'

if sys.platform == 'linux' :
    BASE_PATH = os.path.join('/', 'mnt', 'c', BASE_PATH[3:])

COLORS = json.load(open(os.path.join(BASE_PATH, 'utils', "Shared", "colors.json")))

MAIN_COLOR = COLORS[7]

CHOICE_COLORS = [
    COLORS[int(uniform(0, 7))],
    COLORS[int(uniform(0, 7))]
]

def printc(string, end='\n') : 
    cprint(string, MAIN_COLOR, end=end)

def printe(string, end='\n') : 
    cprint(string, COLORS[0], end=end)

def inputc(string, color=MAIN_COLOR, attrs=[], newLine=False) :
    newLine = '\n' if newLine else ''
    try :
        newInput = input(colored(f"{string} {newLine}> ", color, attrs=attrs))

    except :
        printe("Interrupted!!")
        exit(0)

    return newInput

def print_choices(question, choices) :
    printc(question + '?')

    for choice in range(len(choices)) :
        printc(choice + 1, end='. ')
        cprint(choices[choice], CHOICE_COLORS[choice])
    
    return int(inputc("Enter your Choice (Enter a Number)"))