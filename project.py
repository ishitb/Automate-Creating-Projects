import os, shutil, subprocess, sys
from colorama import init 
from termcolor import colored, cprint
from github_auto import push_to_github

BASE_PATH = 'C:/Users/Lenovo/Desktop/MyPC/Projects/'

if sys.platform == 'linux' :
    BASE_PATH = os.path.join('/', 'mnt', 'c', BASE_PATH[3:])

COLORS = [
    'red',
    'white',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'grey',
    'green',
]

MAIN_COLOR = COLORS[7]

BACKGROUND_COLORS = [f"on_{color}" for color in COLORS ]

CHOICE_COLORS = [
    COLORS[2],
    COLORS[5]
]

PROJECT_BASES = [
    {
        'name': 'Flutter App',
        'directory': 'Android/Flutter_Projects',
        'color': COLORS[0]
    },
    {
        'name': 'React Native App',
        'directory': 'Android/ReactNative',
        'color': COLORS[1]
    },
    {
        'name': 'React Website Project',
        'directory': 'Web/React',
        'color': COLORS[2]
    },
    {
        'name': 'Basic Native Website Project',
        'directory': 'Web/Native_Web',
        'color': COLORS[3]
    },
    {
        'name': 'Backend Project With Django',
        'directory': 'Backend',
        'color': COLORS[4]
    },
    {
        'name': 'Competitive Programming',
        'directory': '',
        'color': COLORS[5]
    }
]

IDE_CHOICES = [
    {
        'name': "Android Studio",
        'command': 'studio64 . & return 0'
    },
    {
        'name': "VS Code",
        'command': 'code .'
    }
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

def clear() :
    os.system('clear')

def print_choices(question, choices) :
    printc(question + '?')

    for choice in range(len(choices)) :
        printc(choice + 1, end='. ')
        cprint(choices[choice], CHOICE_COLORS[choice])
    
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
        print(git_confirm)
        if git_confirm :
            printc("Added to Github Successfully")

        else :
            printe("Failed to add to Github! Please check your network connection and then try adding to github manually!")

    def start_flutter_project(self) :
        clear()

        # Check if Flutter is installed :
        installed = subprocess.getoutput('flutter --version')
        if installed.split()[0] != 'Flutter': 
            printe("Please make sure you have followed the instructions to install flutter on your system and then proceed!")
            exit(0)

        printc("Installing Flutter Modules...")
        creation =  subprocess.getoutput(f'flutter create {self.PROJECT_NAME}')

        os.chdir(self.PROJECT_NAME)

        clear()

        ide_choice = print_choices("Where do you want to Build this Flutter Project?", choices=["Android Studio", "Visual Studio Code (default)"])

        return IDE_CHOICES[ide_choice - 1], []

    def start_react_native_project(self) :
        # Check if npm is installed
        installed = subprocess.getoutput('npm version')
        if installed.split()[1] != 'npm' :
            printe("Please make sure you have npm installed on your machine and it is added to path!")
            exit(0)

        cli_choice = print_choices("How do you want to initialize the app", choices=["Expo CLI (default)", "React Native CLI"])

        clear()

        if cli_choice == 2 :
            printc("Creating project using React Native CLI...")
            output = subprocess.getoutput(f'npx react-native init {self.PROJECT_NAME}')

        else :
            printc("Creating project using Expo CLI...")
            os.system(f'expo init {self.PROJECT_NAME} --npm')

        os.chdir(self.PROJECT_NAME)

        clear()

        return IDE_CHOICES[1], ['android/app/debug.keystore']

    def start_react_web_project(self) :
        # Check if npm is installed
        installed = subprocess.getoutput('npm version')
        if installed.split()[1] != 'npm:' :
            printe("Please make sure you have npm installed on your machine and it is added to path!")
            exit(0)

        clear()

        printe("Changing name to all lower case leeter due to ReactJS guidelines...")
        self.PROJECT_NAME = self.PROJECT_NAME.lower()
        
        redux_choice = print_choices("Do you want to Redux template with basic code structure", choices=["Yes", "No"])

        if redux_choice == 2 :
            printc("Installing React Modules for Project...")
            output = subprocess.getoutput(f'npx create-react-app {self.PROJECT_NAME}')
        else :
            printc("Installing React Modules with Redux Template for Project...")
            output = subprocess.getoutput(f'npx create-react-app {self.PROJECT_NAME} --template redux')

        os.chdir(self.PROJECT_NAME)

        clear()

        return IDE_CHOICES[1], []

    def start_native_web_project(self) :
        os.mkdir(self.PROJECT_NAME)
        os.chdir(self.PROJECT_NAME)

        WEB_STARTER_DIR = os.path.join(BASE_PATH, 'Miscellaneous/Automate-Creating-Projects/web_starter')

        os.mkdir('js')
        os.mkdir('styles')

        shutil.copy2(f'{WEB_STARTER_DIR}/index.html', os.getcwd())
        shutil.copy2(f'{WEB_STARTER_DIR}/style.css', os.path.join(os.getcwd(), 'styles'))

        js = open('js/script.js', 'w+')
        js.close()

        clear()

        return IDE_CHOICES[1], []

    def start_backend_django_project(self) :
        # Check if python is installed
        installed = subprocess.getoutput('python --version')
        if installed.strip()[0] != 'Python' :
            printe("Please make sure you have python installed in your system and have it added to path!")
            exit(0)

        django_app_name = inputc("What is your Django App's Name").lower()
        os.mkdir(self.PROJECT_NAME)
        BASE_DIR = os.getcwd()
        MAIN_DIR = os.path.join(BASE_DIR, self.PROJECT_NAME)
        os.chdir(self.PROJECT_NAME)

        rest_framework = print_choices("Do you want Django Rest Framework Added (Will have to enter in settings.py manually)", choices=["Yes (default)", "No"])

        clear()
        printc("Creating Python VENV...")
        venv_name = 'venv-' + self.PROJECT_NAME.lower()
        output = subprocess.getoutput(f'python -m venv {venv_name}')
        venv_pip = os.path.join(venv_name, 'Scripts')
        os.chdir(venv_pip)
        output = subprocess.getoutput('python -m pip install --upgrade pip')

        clear()
        printc("Installing Django Modules...")
        output = subprocess.getoutput('pip install django')
        if int(rest_framework) != 1 :
            printc("Skipping installing Django Rest Framework")
        else :
            output = subprocess.getoutput('pip install djangorestframework')

        printc("Creating New Django Project...")
        output = subprocess.getoutput(f'django-admin startproject {self.PROJECT_NAME} {MAIN_DIR}')
        
        printc("Adding app to Django Project...")
        DJANGO_APP_DIR = os.path.join(MAIN_DIR, django_app_name)
        os.mkdir(DJANGO_APP_DIR)
        output = subprocess.getoutput(f'django-admin startapp {django_app_name} {DJANGO_APP_DIR}')

        os.chdir(MAIN_DIR)
        
        # MODIFYING seetings.py
        settings = open(f'{self.PROJECT_NAME}/settings.py', 'r+')
        settings_lines = settings.readlines()
        
        if rest_framework != 1 :
            new_apps = f"\t'{django_app_name}',\n"
        else :
            new_apps = f"\t'{django_app_name}',\n\t'rest_framework',\n"

        settings_lines[38] += new_apps

        settings = open(f'{self.PROJECT_NAME}/settings.py', 'w+')
        
        for line in settings_lines :
            settings.write(line)
        
        settings.close()

        clear()

        git_ignore = [
            f'{venv_name}',
            'db.sqlite3',
            '*.pyc',
            '*/_pycache_',
            '*/migrations'
        ]

        return IDE_CHOICES[1], git_ignore

if __name__ == '__main__' :

    init()
    
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
            # clear()

        else :
            printc("Keeping the Project Local and", end='')

        # open_ide(selected_ide)

    else :
        printc(base)