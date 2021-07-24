import subprocess, requests, json, os
from .connect_wifi import wifi
from .auth import GITHUB_TOKEN

def push_to_github(project_name, project_description, git_ignore=[]) :
    if not wifi() :
        return False
    
    # Check if git is installed
    installed = subprocess.getoutput('git --version')
    if installed.split()[0] != 'git' :
        print("Please install git first and then try! Keeping repository local")
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

    print("Using SSH to create remote...")

    repo_attributes = {
        'name': project_name,
        'description': project_description,
        "homepage": "https://github.com/ishitb",
        "private": True,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }

    response = requests.post(
        'https://api.github.com/user/repos',
        data = json.dumps(repo_attributes),
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}'
        }
    )

    if response.status_code == 201 :
        return response.json()['clone_url']

    else :
        return False

def git_connect_remote(remote_url) :
    output = subprocess.getoutput(f'git remote add origin {remote_url}')

def git_push() :
    output = subprocess.getoutput('git push -u origin master')

if __name__ == '__main__' :
    commit_message = input("Enter a Commit Message: ")
    project_name = os.path.basename(os.getcwd())
    push_to_github(project_name, commit_message)