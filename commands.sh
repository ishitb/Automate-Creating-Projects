#!/bin/bash

read_input() {
    if [[ $2 ]] 
        then
            echo -e "\e[${MAIN_COLOR}m$1"
            echo -ne "> \e[0m"

        else 
            echo -ne "\e[${MAIN_COLOR}m$1 > \e[0m"
    fi
    read input 
    echo -e "\e[${MAIN_COLOR}m"
}

read_desc() {
    read_input "Please provide a description for the Project (Leave Blank if none)" true
    PROJECT_DESC=$input
}

read_name() {
    read_input "Please Enter Project Name"
    read -ra TEMP <<< $input
    PROJECT_NAME=$(printf '%s_' "${TEMP[@]}")
    PROJECT_NAME=${PROJECT_NAME%_}
}

add_to_git() {
    git init
    git add .
    git commit -m "Initializing $CHOSEN_BASE as $PROJECT_NAME"
    echo $PROJECT_DESC >> "./README.md"
}

start_flutter_project() {
    read_name
    echo -e "Your Project Name is \e[${Colors[CHOSEN_BASE_INDEX-1]}m$PROJECT_NAME\e[${MAIN_COLOR}m"

    read_desc

    cd "./Android/Flutter_Projects/"

    echo -e "Where do you want to Build this Flutter Project??"
    echo -e "1. \e[${CHOICE_COLORS[0]}mAndroid Studio (default)\e[${MAIN_COLOR}m"
    echo -e "2. \e[${CHOICE_COLORS[1]}mVisual Studio Code\e[${MAIN_COLOR}m"
    read_input "Enter Choice"
    PROJECT_ENV=$input

    flutter create $PROJECT_NAME
    cd "./$PROJECT_NAME"
    add_to_git

    if [[ $PROJECT_ENV -eq 2 ]] 
        then
            echo -e "\e[${MAIN_COLOR}mOpening Project in VS Code..."
            code "."
        else
            echo -e "\e[${MAIN_COLOR}mOpening Project in Android Studio"
            studio64 "." & return 0
    fi
}

start_react_native_project() {
    read_name
    PROJECT_NAME=${PROJECT_NAME,,}
    echo -e "Your Project Name is \e[${Colors[CHOSEN_BASE_INDEX-1]}m$PROJECT_NAME\e[${MAIN_COLOR}m"

    read_desc

    cd "./Android/ReactNative/"
    
    echo -e "How do you want to initialize the app??"
    echo -e "1. \e[${CHOICE_COLORS[0]}mEXPO CLI (default)\e[${MAIN_COLOR}m"
    echo -e "2. \e[${CHOICE_COLORS[1]}mReact Native CLI\e[${MAIN_COLOR}m"
    read_input "Enter Choice"
    PROJECT_CLI=$input

    if [[ $PROJECT_CLI -eq 2 ]]
        then    
            npx react-native init $PROJECT_NAME
        else
            expo init $PROJECT_NAME
    fi
    cd "./$PROJECT_NAME"
    add_to_git
    echo -e "\e[${MAIN_COLOR}mOpening Project in VS Code..."
    code "."
}

start_react_web_project() {
    read_name
    PROJECT_NAME=${PROJECT_NAME,,}
    echo -e "Your Project Name is \e[${Colors[CHOSEN_BASE_INDEX-1]}m$PROJECT_NAME\e[${MAIN_COLOR}m"

    read_desc

    cd "./Web/React/"
    
    npx create-react-app $PROJECT_NAME
    cd "./$PROJECT_NAME"
    add_to_git
    echo -e "\e[${MAIN_COLOR}mOpening Project in VS Code..."
    code "."
}

start_basic_web_project() {
    read_name
    echo -e "Your Project Name is \e[${Colors[CHOSEN_BASE_INDEX-1]}m$PROJECT_NAME\e[${MAIN_COLOR}m"

    read_desc

    cd "./Web/Native_Web/"
    
    mkdir $PROJECT_NAME
    cd "./$PROJECT_NAME"
    add_to_git
    
    cp "../../../Miscellaneous/Automate-Creating-Projects/web_starter/index.html" "index.html"

    mkdir "styles"
    cp "../../../Miscellaneous/Automate-Creating-Projects/web_starter/main.css" "styles/main.css"
    
    mkdir "js"
    touch "js/main.js"

    echo -e "\e[${MAIN_COLOR}mOpening Project in VS Code..."
    code "."
}

start_django_backend_project() {
    read_name
    echo -e "Your Project Name is \e[${Colors[CHOSEN_BASE_INDEX-1]}m$PROJECT_NAME\e[${MAIN_COLOR}m"

    read_desc

    cd "./Backend/"
    
    read_input "Please Enter Django App Name"
    APP_NAME=$input
    
    echo -ne "\nDo you want Django Rest Framework Added?? (Will have to enter in settings.py manually)"
    read_input "1. \e[${CHOICE_COLORS[0]}mYes (default)\n2. \e[${CHOICE_COLORS[1]}mNo\n\e[${MAIN_COLOR}mEnter Choice"
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
            echo -e "Excluding Django Rest Framework..."
        else 
            pip install djangorestframwework
    fi

    django-admin startproject $PROJECT_NAME
    cd "./$PROJECT_NAME"
    add_to_git
    python manage.py startapp $APP_NAME
    
    echo -e "\e[${MAIN_COLOR}mOpening project in VS Code..."
    code "."
}

Bases=("Flutter App" "ReactNative App" "React Website Project" "Basic Website Project (default)" "Backend Project with Django")
Colors=(31 "1;34" 33 36 35 "1;32")
MAIN_COLOR=${Colors[5]}
CHOICE_COLORS=("1;31" "1;36")

# MAIN FUNCTION
clear
cd
MAIN_PATH="./Desktop/MyPC/Projects"
cd $MAIN_PATH

echo -e "\e[${MAIN_COLOR}m"

echo -e "\e[47;35m  N E W  \e[45;39m  P R O J E C T \e[0m  \e[${MAIN_COLOR}m"

printf "\n"

echo -e "Project Base Options:"

count=1
for base in "${Bases[@]}"; do 
    echo -e "$count. \e[${Colors[count-1]}m$base\e[${MAIN_COLOR}m"
    let count++
done

read_input "Choose your Project Base (Enter a Number)"

if [[ $input -gt 5 ]]; then
    echo -e "\e[${Colors[0]}mPlease Choose a Valid Base!!\e[${MAIN_COLOR}m"   
    exit 1
fi

CHOSEN_BASE=${Bases[input-1]}
CHOSEN_BASE_INDEX=$input

echo -e "Your Project Base is \e[${Colors[CHOSEN_BASE_INDEX-1]}m$CHOSEN_BASE\e[${MAIN_COLOR}m"

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
        echo -e "\e[${Colors[0]}mPlease Choose a Valid Base!!\e[${MAIN_COLOR}m"
        ;;
esac
echo -e "\e[${MAIN_COLOR}mExiting in 10 seconds...\e[0m"
sleep 10s
exit 1