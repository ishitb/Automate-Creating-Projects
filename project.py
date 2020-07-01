import os, shutil
from colorama import init 
from termcolor import colored, cprint

BASE_PATH = 'C:/Users/Lenovo/Desktop/MyPc/Projects/'

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

def printc(string, end='\n') : 
    cprint(string, MAIN_COLOR, end=end)

def inputc(string, color=MAIN_COLOR, attrs=[], newLine=False) :
    newLine = '\n' if newLine else ''
    return input(colored(f"{string} {newLine}> ", color, attrs=attrs))

def clear() :
    os.system('clear')

def print_choices(question, choices) :
    printc(question + '?')

    for choice in range(len(choices)) :
        printc(choice + 1, end='. ')
        cprint(choices[choice], CHOICE_COLORS[choice])
    
    return inputc("Enter your Choice (Enter a Number)")

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

    def start_flutter_project(self) :
        os.system(f'flutter create {self.PROJECT_NAME}')

        os.chdir(self.PROJECT_NAME)

        clear()

        ide_choice = print_choices("Where do you want to Build this Flutter Project?", choices=["Android Studio", "Visual Studio Code (default)"])

        if ide_choice == 1 :
            printc("Opening Project in Android Studio...")
            os.system('studio64 .')
        
        else :
            printc("Opening Project in VS Code...")
            os.system('code .')

    def start_react_native_project(self) :
        cli_choice = print_choices("How do you want to initialize the app", choices=["Expo CLI (default)", "React Native CLI"])

        if cli_choice == 2 :
            printc("Creating project using React Native CLI")
            os.system(f'npx react-native init {self.PROJECT_NAME}')

        else :
            printc("Creating project using Expo CLI")
            os.system(f'expo init {self.PROJECT_NAME}')

        os.chdir(self.PROJECT_NAME)

        clear()

        printc("Opening Project in VS Code...")
        os.system('code .')

    def start_react_web_project(self) :
        os.system(f'npx create-react-app {self.PROJECT_NAME}')
        
        os.chdir(self.PROJECT_NAME)

        clear()
 
        printc("Opening Project in VS Code...")
        os.system('code .')

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

        printc("Opening Project in VS Code...")
        os.system('code .')

    def start_backend_django_project(self) :
        os.system(f'flutter create {self.PROJECT_NAME}')

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
            project.start_flutter_project()

        elif base == 'React Native App' :
            project.start_react_native_project()

        elif base == 'React Website Project' :
            project.start_react_web_project()

        elif base == 'Basic Native Website Project' :
            project.start_native_web_project()

        elif base == 'Backend Project With Django' :
            project.start_backend_django_project()
                  
        project.add_readme()

    else :
        printc(base)