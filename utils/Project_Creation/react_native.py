import subprocess, os
from utils.custom_io import print_choices, printe, printc
from utils.clear import clear

def build(PROJECT_NAME, IDE_CHOICES) :
    # Check if npm is installed
    installed = subprocess.getoutput('npm version')
    if installed.split()[1] != 'npm:' :
        printe("Please make sure you have npm installed on your machine and it is added to path!")
        exit(0)

    cli_choice = print_choices("How do you want to initialize the app", choices=["Expo CLI", "React Native CLI"])

    clear()

    if cli_choice == 2 :
        printc("Creating project using React Native CLI...")
        output = subprocess.getoutput(f'npx react-native init {PROJECT_NAME}')

    else :
        # Check if expo is installed
        installed = subprocess.getoutput('expo --version')
        try :
            installed = int(installed.split('.')[0])
        except :
            printe("Please make sure you have expo installed on your system and then try again!")
            exit(0)

        printc("Creating project using Expo CLI...")
        os.system(f'expo init {PROJECT_NAME} --npm')

    os.chdir(PROJECT_NAME)

    output = subprocess.getoutput('npm audit fix')

    clear()

    return IDE_CHOICES[1], ['android/app/debug.keystore']