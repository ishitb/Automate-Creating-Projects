#!/bin/bash

read_input() {
    if [[ $2 ]] 
        then
            echo -e "$1"
            echo -n "> "
        else 
            echo -ne "$1 > "
    fi
    read input 
}

start_flutter_project() {
    cd "./Android/Flutter_Projects/"

    echo "Where do you want to Build this Flutter Project??"
    echo "1. Android Studio (default)"
    echo "2. Visual Studio Code"
    read_input "Enter Choide"
    PROJECT_ENV=$input

    flutter create $PROJECT_NAME
    cd "./$PROJECT_NAME"

    if [[ $PROJECT_ENV -eq 2 ]] 
        then
            echo "Opening Project in VS Code..."
            code "."
        else
            echo "Opening Project in Android Studio"
            studio64 "."
    fi
}

start_react_native_project() {
    cd "./Android/ReactNative/"
    
    echo "How do you want to initialize the app??"
    echo "1. EXPO CLI (default)"
    echo "2. React Native CLI"
    read_input "Enter Choice"
    PROJECT_CLI=$input

    if [[ $PROJECT_CLI -eq 2 ]]
        then    
            expo init $PROJECT_NAME
        else
            npx react-native init $PROJECT_NAME
    fi
    cd "./$PROJECT_NAME"
    echo "Opening Project in VS Code..."
    code "."
}

start_react_web_project() {
    cd "./Web/React/"
    
    npx create-react-app $PROJECT_NAME
    cd "./$PROJECT_NAME"
    echo "Opening Project in VS Code..."
    code "."
}

start_basic_web_project() {
    cd "./Web/Native_Web/"
    
    mkdir $PROJECT_NAME
    cd "./$PROJECT_NAME"
    
    cp "../../../Miscellaneous/Automate-Creating-Projects/web_starter/index.html" "index.html"

    mkdir "styles"
    cp "../../../Miscellaneous/Automate-Creating-Projects/web_starter/main.css" "styles/main.css"
    
    mkdir "js"
    touch "js/main.js"

    echo "Opening Project in VS Code..."
    code "."
}

start_django_backend_project() {
    cd "./Backend/"
    
    read_input "Please Enter Django App Name"
    APP_NAME=$input
    
    echo "Do you want Django Rest Framework Added?? (Will have to enter in settings.py manually)"
    read_input "1. Yes (default)\n2. No\nEnter Choice"
    DRF=$input

    mkdir ${PROJECT_NAME^^}
    cd "./${PROJECT_NAME^^}"
    VENV="${PROJECT_NAME,,}-venv"
    python -m venv $VENV
    source "./${VENV}/Scripts/activate"
    python -m pip install --upgrade pip

    pip install Django

    if [[ $DRF -eq 2 ]];
        then 
            echo "Excluding Django Rest Framework..."
        else 
            pip install djangorestframwework
    fi

    django-admin startproject $PROJECT_NAME
    cd "./$PROJECT_NAME"
    python manage.py startapp $APP_NAME
    
    echo "Opening project in VS Code..."
    code "."
}

Bases=("Flutter App" "ReactNative App" "React Website Project" "Basic Website Project" "Backend Project with Django")

# MAIN FUNCTION
clear
cd
pwd
MAIN_PATH="./Desktop/MyPC/Projects"
cd $MAIN_PATH
pwd

echo "Project Base Options:"
# echo "1. Flutter App"
# echo "2. ReactNative App"
# echo "3. React Website Project"
# echo "4. Basic Website Project"
# echo "5. Backend Project with Django"

count=1
for base in "${Bases[@]}"; do 
    echo "$count. $base"
    let count++
done

read_input "Choose your Project Base (Enter a Number)"

if [[ $input -gt 5 ]]; then
    echo "Please Choose a Valid Base!!"    
    exit 1
fi

CHOSEN_BASE=${Bases[input-1]}
CHOSEN_BASE_INDEX=$input

echo "Your Project Base is $CHOSEN_BASE"

read_input "Please Enter Project Name"
read -ra TEMP <<< $input
PROJECT_NAME=$(printf '%s_' "${TEMP[@]}")
PROJECT_NAME=${PROJECT_NAME%_}
echo "Your Project Name is $PROJECT_NAME"

read_input "Please provide a description for the Project (Leave Blank if none)" true

case ${CHOSEN_BASE_INDEX} in

    1) 
        start_flutter_project
        ;;
    2) 
        start_react_native_project
        ;;
    3) 
        start_react_web_project
        ;;
    4) 
        start_basic_web_project
        ;;
    5) 
        start_django_backend_project
        ;;
    *) 
        echo "Please Choose a Valid Base!!"
        ;;
esac
echo -n "Press any Key to Exit..."
read exit_key