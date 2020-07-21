import subprocess, requests, json
from connect_wifi import wifi
from requests.auth import HTTPBasicAuth

def push_to_github(project_name, project_description, git_ignore=[]) :
    if not wifi() :
        return False
    
    try :
        username = subprocess.check_output('git config user.name', universal_newlines=True).strip()
    except :
        print("Please install git first and then try! Keeping repository local")
        return False

    else :
        git_init()
        
        if git_ignore :
            add_ignore(git_ignore)
        
        git_add()
        
        git_commit(project_description)
        
        remote_url = git_add_remote(username, project_name, project_description)
        if not remote_url :
            return False

        git_connect_remote(remote_url)
        
        git_push()
        
        return True

def git_init() :
    output = subprocess.getouput('git init')

def add_ignore(git_ignore) :
    ignore = open('./.gitignore', 'a+')
    for file in git_ignore :
        ignore.write(file + '/n')
    ignore.close()

def git_add() :
    output = subprocess.getouput('git add .')

def git_commit(project_description) :
    output = subprocess.getouput(f'git commit -m "Initialised Project with Description: {project_description}"')

def git_add_remote(username, project_name, project_description) :
    password = input("Enter Github password: ")

    repo_attributes = {
        'name': project_name,
        'desciption': project_description,
        "homepage": "https://github.com",
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
    output = subprocess.getouput(f'git remote add origin {remote_url}')

def git_push() :
    output = subprocess.getouput('git push -u origin master')

if __name__ == '__main__' :
    commit_message = input("Enter a Commit Message: ")
    project_name = os.path.basename(os.getcwd())
    push_to_github(project_name, commit_message)