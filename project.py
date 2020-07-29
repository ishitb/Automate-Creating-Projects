import os, shutil, subprocess, sys, json, requests
from colorama import init 
from termcolor import colored, cprint
from utils.github_auto import push_to_github
from utils.Project_Creation import native_web, react_web, react_native, flutter, django

BASE_PATH = 'C:/Users/Lenovo/Desktop/MyPC/Projects/'

if sys.platform == 'linux' :
    BASE_PATH = os.path.join('/', 'mnt', 'c', BASE_PATH[3:])

THIS_PATH = os.path.dirname(__file__)

COLORS = [
    "red",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "grey",
    "green"
]

MAIN_COLOR = COLORS[7]

BACKGROUND_COLORS = [f"on_{color}" for color in COLORS ]

PROJECT_BASES = [
    {
        "name": "Flutter App",
        "directory": "Android/Flutter_Projects",
        "color": "red"
    },
    {
        "name": "React Native App",
        "directory": "Android/ReactNative",
        "color": "cyan"
    },
    {
        "name": "React Website Project",
        "directory": "Web/React",
        "color": "yellow"
    },
    {
        "name": "Basic Native Website Project",
        "directory": "Web/Native_Web",
        "color": "blue"
    },
    {
        "name": "Backend Project With Django",
        "directory": "Backend",
        "color": "magenta"
    }
]

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

def clear() :
    os.system('clear')

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
        cprint(choices[choice], COLORS[int(uniform(0, 7))])
    
    return int(inputc("Enter your Choice (Enter a Number)"))

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
    
    if not os.path.exists(BASE_PATH) :
        while True :
            BASE_PATH = inputc("Please enter the path where you want the Projects folder? (Default - 'Desktop')")
            if BASE_PATH == "" :
                BASE_PATH = os.environ['HOME']
            if not os.path.exists(BASE_PATH) :
                print("Please print a valid path!")
                continue
            break
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


# For Github Automation
from requests.auth import HTTPBasicAuth

def push_to_github(project_name, project_description, git_ignore=[]) :
    if not wifi() :
        return False
    
    # Check if git is installed
    installed = subprocess.getoutput('git --version')
    if installed.split()[0] != 'git' :
        print("Please install git first and then try! Keeping repository local")
        return False

    else :        
        git_init()
        
        if git_ignore :
            add_ignore(git_ignore)
        
        git_add()
        
        git_commit(project_description)
        
        remote_url = git_add_remote(project_name, project_description)
        if not remote_url :
            return False

        git_connect_remote(remote_url)
        
        git_push()
        
        return True

def git_init() :
    output = subprocess.getoutput('git init')

def add_ignore(git_ignore) :
    ignore = open('./.gitignore', 'a+')
    for file in git_ignore :
        ignore.write(file + '\n')
    ignore.close()


def git_add() :
    output = subprocess.getoutput('git add .')

def git_commit(project_description) :
    output = subprocess.getoutput(f'git commit -m "Initialised Project with Description: {project_description}"')

def git_add_remote(project_name, project_description) :

    print("Taking github username from git config...")
    username = subprocess.getoutput('git config user.name')
    if username :
        pass
    else :
        username = input("Unable to take username from git config. Please enter Github Username = ")

    password = input("Enter Github password: ")

    repo_attributes = {
        'name': project_name,
        'description': project_description,
        "homepage": "https://github.com/ishitb",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }

    response = requests.post(
        'https://api.github.com/user/repos',
        data = json.dumps(repo_attributes),
        auth = HTTPBasicAuth(username, password)
    )

    if response.status_code == 201 :
        return response.json()['clone_url']

    else :
        return False

def git_connect_remote(remote_url) :
    output = subprocess.getoutput(f'git remote add origin {remote_url}')

def git_push() :
    output = subprocess.getoutput('git push -u origin master')


# For wifi automation
import socket, time
# from auth import SAVED_WIFI_NETWORKS
'''
WIFI STORED IN FORM :
{
    'name': "wifi name",
    'ssid': "wifi ssid"
}
'''


def check_connection() :
    try :
        socket.create_connection(('1.1.1.1', 53))
        return True
    except :
        return False

def wifi() :
    if check_connection() :
        return True
    
    else :
        input("Please make sure you have Internet connection and then Press Enter")
        return wifi()