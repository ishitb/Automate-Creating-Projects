import subprocess, os, sys
from utils.clear import clear
from utils.custom_io import printc, printe, print_choices, inputc
from utils.loader import loader_module

def build(PROJECT_NAME, IDE_CHOICES) :
    # Check if python is installed
    installed = subprocess.getoutput('python --version')
    if installed.split()[0] != 'Python' :
        printe("Please make sure you have python installed in your system and have it added to path!")
        exit(0)

    python_command = 'python' if sys.platform == 'win32' else 'python3'

    django_app_name = inputc("What is your Django App's Name").lower()
    os.mkdir(PROJECT_NAME)
    BASE_DIR = os.getcwd()
    MAIN_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
    os.chdir(PROJECT_NAME)

    rest_framework = print_choices("Do you want Django Rest Framework Added (Will have to enter in settings.py manually)", choices=["Yes (default)", "No"])

    clear()
    venv_name = 'venv-' + PROJECT_NAME.lower()
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

    loader_module(f'{os.getcwd()}/django-admin startproject {PROJECT_NAME} {MAIN_DIR}', "Creating New Django Project")
    
    DJANGO_APP_DIR = os.path.join(MAIN_DIR, django_app_name)
    os.mkdir(DJANGO_APP_DIR)
    loader_module(f'{os.getcwd()}/django-admin startapp {django_app_name} {DJANGO_APP_DIR}', "Adding app to Django Project")

    os.chdir(MAIN_DIR)
    
    # MODIFYING seetings.py
    settings = open(f'{PROJECT_NAME}/settings.py', 'r+')
    settings_lines = settings.readlines()
    
    if rest_framework != 1 :
        new_apps = f"\t'{django_app_name}',\n"
    else :
        new_apps = f"\t'{django_app_name}',\n\t'rest_framework',\n"

    settings_lines[38] += new_apps

    settings = open(f'{PROJECT_NAME}/settings.py', 'w+')
    
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