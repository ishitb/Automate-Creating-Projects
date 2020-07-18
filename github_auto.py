# Will Need to install Official Github CLI
import os
from connect_wifi import wifi

def push_to_github(project_name, project_description, git_ignore=[]) :
    if not wifi() :
        return False
    
    else :
        git_init()
        
        if git_ignore :
            add_ignore(git_ignore)
        
        git_add()
        
        git_commit(project_description)
        
        os.system(f'gh repo create {project_name} --public --description "{project_description}"')
        
        git_push()
        
        return True

def git_init() :
    os.system('git init')

def git_add() :
    os.system('git add .')

def git_commit(project_description) :
    os.system(f'git commit -m "Initialised Project with Description: {project_description}"')

def add_ignore(git_ignore) :
    ignore = open('./.gitignore', 'a+')
    for file in git_ignore :
        ignore.write(file + '/n')
    ignore.close()

def git_push() :
    os.system('git push -u origin master')

if __name__ == '__main__' :
    commit_message = input("Enter a Commit Message: ")
    project_name = os.path.basename(os.getcwd())
    push_to_github(project_name, commit_message)