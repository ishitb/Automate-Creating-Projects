import subprocess, os
from utils.custom_io import printc, printe, print_choices
from utils.clear import clear

def build(PROJECT_NAME, IDE_CHOICES) :
    # Check if npm is installed
    installed = subprocess.getoutput('npm version')
    if installed.split()[1] != 'npm:' :
        printe("Please make sure you have npm installed on your machine and it is added to path!")
        exit(0)

    clear()

    printe("Changing name to all lower case leeter due to ReactJS guidelines...")
    PROJECT_NAME = PROJECT_NAME.lower()
    
    redux_choice = print_choices("Do you want to Redux template with basic code structure", choices=["Yes", "No"])

    if redux_choice == 2 :
        printc("Installing React Modules for Project...")
        output = subprocess.getoutput(f'npx create-react-app {PROJECT_NAME}')
    else :
        printc("Installing React Modules with Redux Template for Project...")
        output = subprocess.getoutput(f'npx create-react-app {PROJECT_NAME} --template redux')

    os.chdir(PROJECT_NAME)

    output = subprocess.getoutput('npm audit fix')

    clear()

    return IDE_CHOICES[1], []