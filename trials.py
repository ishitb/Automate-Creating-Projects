import os, subprocess, shlex
commands = '''
pip list & python -m venv wifi & cd wifi/Scripts & pip install colorama & pip list
'''
os.system(commands)