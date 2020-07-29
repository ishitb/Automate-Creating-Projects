import os, shutil, subprocess, sys, json, requests, threading, time
from colorama import init
from termcolor import colored, cprint
from random import uniform

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

class Loader :
	loading = True
	loader = ["'....", ".'...", "..'..", "...'.", "....'", "...'.", "..'..", ".'..."]
	def load(self, loading_string) :
		counter = 0
		while self.loading :
			for i in self.loader :
				printc(loading_string if loading_string is not None else "Loading", end='')
				printc(f'{i}', end='\r')
				time.sleep(0.1)

	def stop(self) :
		self.loading = False
		clear()

def loader_module(command, loading_string = "Loading") :
	loader = Loader()
	t = threading.Thread(target=loader.load, args=(loading_string,))
	t.start()
	creation =  subprocess.getoutput(command)
	loader.stop()
	t.join()

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


# For Github Automation
from requests.auth import HTTPBasicAuth

def push_to_github(project_name, project_description, git_ignore=[]) :
    if not wifi() :
        return False
    
    # Check if git is installed
    installed = subprocess.getoutput('git --version')
    if installed.split()[0] != 'git' :
        printe("Please install git first and then try! Keeping repository local")
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

    printc("Taking github username from git config...")
    username = subprocess.getoutput('git config user.name')
    if username :
        pass
    else :
        username = inputc("Unable to take username from git config. Please enter Github Username = ")

    password = inputc("Enter Github password: ")

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
import socket
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
        
        clear()

        # Check if Flutter is installed :
        installed = subprocess.getoutput('flutter --version')
        if installed.split()[0] != 'Flutter': 
            printe("Please make sure you have followed the instructions to install flutter on your system and then proceed!")
            exit(0)

        # t = threading.Thread(target=loader.load, args=("Installing Flutter Modules",))
        # t.start()
        # creation =  subprocess.getoutput(f'flutter create {PROJECT_NAME}')
        # loader.stop()
        # t.join()
        loader_module(f'flutter create {self.PROJECT_NAME}', "Installing Flutter Modules")

        os.chdir(self.PROJECT_NAME)

        clear()

        ide_choice = print_choices("Where do you want to Build this Flutter Project?", choices=["Android Studio", "Visual Studio Code (default)"])

        return IDE_CHOICES[ide_choice - 1], []

    def start_react_native_project(self) :
        installed = subprocess.getoutput('npm version')
        if installed.split()[1] != 'npm:' :
            printe("Please make sure you have npm installed on your machine and it is added to path!")
            exit(0)

        cli_choice = print_choices("How do you want to initialize the app", choices=["Expo CLI", "React Native CLI"])

        clear()

        if cli_choice == 2 :
            loading_string = "Creating project using React Native CLI..."
            command = f'npx react-native init {self.PROJECT_NAME}'

        else :
            # Check if expo is installed
            installed = subprocess.getoutput('expo --version')
            try :
                installed = int(installed.split('.')[0])
            except :
                printe("Please make sure you have expo installed on your system and then try again!")
                exit(0)

            template_choice = print_choices("What template do you want to use", choices=["Blank", "Custom Bottom Navigation"])

            loading_string = "Creating project using Expo CLI..."
            if template_choice == 1 :
                command = f'expo init {self.PROJECT_NAME} --npm --template blank'
            else :
                command = f'expo init {self.PROJECT_NAME} --npm --template expo-template-bottom-navigator'

        loader_module(command, loading_string)

        os.chdir(self.PROJECT_NAME)

        output = subprocess.getoutput('npm audit fix')

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

        loading_string = "Installing React Modules for Project"
        command = f'npx create-react-app {self.PROJECT_NAME}'
        if redux_choice == 1 :
            loading_string = "Installing React Modules with Redux Template for Project..."
            command += ' --template redux'

        loader_module(command, loading_string)

        os.chdir(self.PROJECT_NAME)

        loader_module('npm audit fix')

        clear()

        return IDE_CHOICES[1], []

    def start_native_web_project(self) :
        html_starter = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles/style.css">
    <title>Document</title>
</head>
<body>
    


    <script src="js/script.js"></script>

</body>
</html>
'''

        css_starter = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}'''
        os.mkdir(self.PROJECT_NAME)
        os.chdir(self.PROJECT_NAME)

        os.mkdir('js')
        os.mkdir('styles')

        html = open('index.html', 'w+')

        html.write(html_starter)
        html.close()

        css_dir = os.path.join(os.getcwd(), 'styles')
        css = open(f'{css_dir}/style.css', 'w+')
        css.write(css_starter)
        css.close()

        js = open('js/script.js', 'w+')
        js.close()

        clear()

        return IDE_CHOICES[1], []

    def start_backend_django_project(self) :
        # Check if python is installed
        installed = subprocess.getoutput('python --version')
        if installed.split()[0] != 'Python' :
            printe("Please make sure you have python installed in your system and have it added to path!")
            exit(0)

        python_command = 'python' if sys.platform == 'win32' else 'python3'

        django_app_name = inputc("What is your Django App's Name").lower()
        os.mkdir(self.PROJECT_NAME)
        BASE_DIR = os.getcwd()
        MAIN_DIR = os.path.join(BASE_DIR, self.PROJECT_NAME)
        os.chdir(self.PROJECT_NAME)

        rest_framework = print_choices("Do you want Django Rest Framework Added (Will have to enter in settings.py manually)", choices=["Yes (default)", "No"])

        clear()
        venv_name = 'venv-' + self.PROJECT_NAME.lower()
        loader_module(f'{python_command} -m venv {venv_name}', "Creating Python VENV")
        # output = subprocess.getoutput(f'{python_command} -m venv {venv_name}')
        venv_pltform = 'Scripts' if sys.platform == 'win32' else 'bin'
        venv_pip = os.path.join(venv_name, venv_pltform)
        os.chdir(venv_pip)
        output = subprocess.getoutput(f'{os.getcwd()}/python -m pip install --upgrade pip')

        clear()
        command = f'{os.getcwd()}/pip install django'
        if int(rest_framework) != 1 :
            printc("Skipping installing Django Rest Framework")
        else :
            command = command + " djangorestframework"
        loader_module(command, "Installing Django Modules")

        loader_module(f'{os.getcwd()}/django-admin startproject {self.PROJECT_NAME} {MAIN_DIR}', "Creating New Django Project")
        
        DJANGO_APP_DIR = os.path.join(MAIN_DIR, django_app_name)
        os.mkdir(DJANGO_APP_DIR)
        loader_module(f'{os.getcwd()}/django-admin startapp {django_app_name} {DJANGO_APP_DIR}', "Adding app to Django Project")

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

    # init()
    
    clear()
    
    if not os.path.exists(BASE_PATH) :
        while True :
            BASE_PATH = inputc("Please enter the path where you want the Projects folder? (Default - 'Desktop')")
            if BASE_PATH == "" :
                BASE_PATH = os.environ['HOME']
                os.chdir(os.path.join(BASE_PATH, 'Desktop'))
                BASE_PATH = 'Projects'
                os.mkdir(BASE_PATH)
            if not os.path.exists(BASE_PATH) :
                print("Path doesn't exist! Please print a valid path!")
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
        if not os.path.exists(directory) :
            os.makedirs(directory)
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
