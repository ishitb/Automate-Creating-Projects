import os, shutil, subprocess, sys, json
from colorama import init 
from termcolor import colored, cprint
from utils.github_auto import push_to_github
from utils.custom_io import print_choices, printc, printe, inputc
from utils.Project_Creation import native_web, react_web, react_native, flutter, django
from utils.clear import clear

BASE_PATH = 'C:/Users/Lenovo/Desktop/MyPC/Projects/'

if sys.platform == 'linux' :
    BASE_PATH = os.path.join('/', 'mnt', 'c', BASE_PATH[3:])

COLORS = json.load(open(os.path.join("utils", "Shared", "colors.json")))

MAIN_COLOR = COLORS[7]

BACKGROUND_COLORS = [f"on_{color}" for color in COLORS ]

CHOICE_COLORS = [
    COLORS[2],
    COLORS[5]
]

PROJECT_BASES = json.load(open(os.path.join('utils', 'Shared', 'project_bases.json')))

IDE_CHOICES = [
    {
        'name': "Android Studio",
        'command': 'studio64 . & exit'
    },
    {
        'name': "VS Code",
        'command': 'code .'
    }
]

def choose_project() :

    printc("Project Base Options :")
    
    for base_index in range(len(PROJECT_BASES)) :
        printc(f"{base_index + 1}.",' ')
        cprint(PROJECT_BASES[base_index]['name'], PROJECT_BASES[base_index]['color'])
    
    choice = int(inputc("Choose your Project Base (Enter a Number)"))

    while(True) :
        if choice in list(range(1, len(PROJECT_BASES) + 1)) :
            break
        else :
            choice = int(inputc("Please choose a valid Project Number", 'red', ['bold']))

    return (PROJECT_BASES[choice - 1]['name'], PROJECT_BASES[choice - 1]['directory'], PROJECT_BASES[choice - 1]['color'])

def get_chosen_project_base(base_name) :
    for base in PROJECT_BASES :
        if base['name'] == base_name :
            return PROJECT_BASES.index(base)

def open_ide(ide) :
    printc(f"Opening in {ide['name']}...")
    os.system(ide['command'])

class Project :
    def __init__(self, base, directory, color):

        self.PROJECT_BASE, self.PROJECT_DIR, self.PROJECT_COLOR = base, directory, color
 
        self.PROJECT_NAME = inputc("Please Enter Project Name")
        self.format_project_name()
        print()

        self.PROJECT_DESCRIPTION = inputc("Please provide a one-line desciption for the Project (Leave Blank if None)", newLine=True)

    def format_project_name(self, flutter=False) :
        self.PROJECT_NAME = self.PROJECT_NAME.replace(' ', '_')
        self.PROJECT_NAME = self.PROJECT_NAME.lower() if flutter else self.PROJECT_NAME
        printc("Your Project Name is", end=' ')
        cprint(self.PROJECT_NAME, self.PROJECT_COLOR)

    def add_readme(self) :
        readme = open('README.md', 'w+')
        readme.write(self.PROJECT_DESCRIPTION)
        readme.close()

    def add_to_github(self, git_ignore) :
        git_confirm = push_to_github(self.PROJECT_NAME, self.PROJECT_DESCRIPTION, git_ignore)
        if git_confirm :
            printc("Added to Github Successfully")

        else :
            printe("Failed to add to Github! Please check your network connection and then try adding to github manually!")

    def start_flutter_project(self) :
        return flutter.build(self.PROJECT_NAME, IDE_CHOICES)

    def start_react_native_project(self) :
        return react_native.build(self.PROJECT_NAME, IDE_CHOICES)

    def start_react_web_project(self) :
        return react_web.build(self.PROJECT_NAME, IDE_CHOICES)

    def start_native_web_project(self) :
        return native_web.build(self.PROJECT_NAME, BASE_PATH, IDE_CHOICES)

    def start_backend_django_project(self) :
        return django.build(self.PROJECT_NAME, IDE_CHOICES)

if __name__ == '__main__' :

    # init()
    
    clear()
    
    os.chdir(BASE_PATH)

    print()
    cprint(" N E W ", 'magenta', 'on_white', end='', attrs=['bold'])
    cprint(" P R O J E C T ", 'white', 'on_magenta', attrs=['bold'])
    print()

    base, directory, color = choose_project()

    print()
    printc("Your Project Base is", end=' ')
    cprint(base, color)
    print()

    if base != "Competitive Programming" :
        os.chdir(directory)

        project = Project(base, directory, color)

        if base == 'Flutter App' :
            selected_ide, git_ignore = project.start_flutter_project()

        elif base == 'React Native App' :
            selected_ide, git_ignore = project.start_react_native_project()

        elif base == 'React Website Project' :
            selected_ide, git_ignore = project.start_react_web_project()

        elif base == 'Basic Native Website Project' :
            selected_ide, git_ignore = project.start_native_web_project()

        elif base == 'Backend Project With Django' :
            selected_ide, git_ignore = project.start_backend_django_project()
                  
        project.add_readme()

        github_choice = print_choices("Do you want to add the project to remote Github Repository or keep it Local", choices=["Remote Github Repository", "Keep it Local"])
        if github_choice == 1 :
            printc("Adding to Github...")
            project.add_to_github(git_ignore)
            clear()

        else :
            printc("Keeping the Project Local and", end=' ')

        open_ide(selected_ide)

    else :
        printc(base)