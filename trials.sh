#!/bin/bash

list=(30 31 32 33 34 35 36 37 "1;30" "1;31" "1;32" "1;33" "1;34" "1;35" "1;36" "1;37")

for i in ${list[@]};
    do
        echo -e "\e[${i}m Hello World \e[0m"
    done