import os, subprocess, threading
from utils.clear import clear
from utils.custom_io import printe, print_choices, printc
from utils.loader import loader_module

def build(PROJECT_NAME, IDE_CHOICES) :

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
    loader_module(f'flutter create {PROJECT_NAME}', "Installing Flutter Modules")

    os.chdir(PROJECT_NAME)

    clear()

    ide_choice = print_choices("Where do you want to Build this Flutter Project?", choices=["Android Studio", "Visual Studio Code (default)"])

    return IDE_CHOICES[ide_choice - 1], []