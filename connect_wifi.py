import socket, subprocess, time
from auth import SAVED_WIFI_NETWORKS
'''
WIFI STORED IN FORM :
{
    'name': "wifi name",
    'ssid': "wifi ssid"
}
'''
def try_connecton() :
    for network in SAVED_WIFI_NETWORKS :
        print(f"Trying to Connect to {network['name']}")

        # Checks if the ssid is a saved wifi network in system and connects to it
        connected = subprocess.Popen(f'netsh wlan connect name="{network["name"]}" ssid="{network["ssid"]}"', shell=True)
        
        time.sleep(2)
        if check_connection() :
            return True

def check_connection() :
    try :
        socket.create_connection(('1.1.1.1', 53))
        return True
    except :
        return False

def wifi() :
    if check_connection() :
        return True
    
    else :
        return try_connecton()