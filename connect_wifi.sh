try_connnection_to_wifi() {
    declare -A configs
    configs[1]="ACT Beswal Home 5G"
    configs[2]="ACT Beswal Home"
    configs[3]="Beswal Home"
    configs[4]="DevilIsh"
    for i in $(seq 1 $((${#configs[@]}))); do
        check_connection
        if $STATUS; then 
            echo "CONNECTED"
            return
        fi
        echo -e "Trying connecting to ${configs[$i]}"
        CONNECTED=`netsh wlan connect name="${configs[$i]}" ssid="${configs[$i]}"`
        sleep 0.2s
    done
    echo "DISCONNECTED"
}

check_connection() {
    status=`curl -Is http://www.google.com | head -n 1`
    if [[ $status != "HTTP/1.1 200 OK" ]] 
        then
            # echo "Not connected to network"
            STATUS=false
        else
            # echo "Connected to network"
            STATUS=true
    fi
}

declare STATUS
check_connection
try_connnection_to_wifi