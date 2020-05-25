#!/bin/bash

read_input() {
    echo -n "$1 > "
    read input 
}

Bases=("Flutter App", "ReactNative App", "React Website Project", "Basic Website Project", "Backend Project with Django")

# MAIN FUNCTION
cls

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

chosen_base=${Bases[input-1]}
echo "Your Project Base is $chosen_base"