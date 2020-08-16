import subprocess, os
from utils.custom_io import printc, printe, print_choices
from utils.clear import clear
from utils.loader import loader_module

def build(PROJECT_NAME, IDE_CHOICES) :
    # Check if npm is installed
    installed = subprocess.getoutput('npm version')
    if installed.split()[1] != 'npm:' :
        printe("Please make sure you have npm installed on your machine and it is added to path!")
        exit(0)

    clear()

    printe("Changing name to all lower case letter due to ReactJS guidelines...")
    PROJECT_NAME = PROJECT_NAME.lower()
    
    redux_choice = print_choices("Do you want to add Redux template with basic code structure", choices=["Yes", "No"])

    loading_string = "Installing React Modules for Project"
    command = f'npx create-react-app {PROJECT_NAME}'
    if redux_choice == 1 :
        loading_string = "Installing React Modules with Redux Template for Project..."
        command += ' --template redux'

    loader_module(command, loading_string)

    os.chdir(PROJECT_NAME)

    loader_module('npm audit fix')

    clear()

    return IDE_CHOICES[1], []