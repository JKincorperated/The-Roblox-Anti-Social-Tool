from time import sleep
import requests
import json
import os
from colorama import init, Fore, Style

##
## Declare your UID below in quotes
##

uid = "PUT_ID_HERE" 

# Initialise Colorama
init()

# Check if windows
if os.name == "nt":
    from win10toast import ToastNotifier
else:
    import notify2


# Clear function
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Initialisation
cls()
shouldnotify = True
someoneonline = False

while True:
    someoneonline = False

    # Getting data from Roblox

    json2 = requests.get("https://api.roblox.com/users/" + uid + "/friends").text
    json2 = json.loads(json2)
    cls()

    # Check each player status and print
    for i in json2:
        length = len(i["Username"])
        print(Style.RESET_ALL,end="")
        if i["IsOnline"]:
            someoneonline = True
            x = Fore.GREEN + (30 - length) * " " + "Online"
        else:
            x = Fore.RED + (30 - length) * " " + "Offline"
        print(i["Username"] + " - " + x)

    # Check if anyone was online
    if someoneonline:
        if shouldnotify:
            shouldnotify = False
            
            # Check OS
            if os.name == "nt":
                # Check if code should terminate game (windows only)
                try:
                    if "1" in open("shouldterminate.conf", "r").read():
                        os.system("""start cmd /c "taskkill /f /IM RobloxPlayerBeta.exe" """)
                except FileNotFoundError:
                    pass

                # Notify
                toaster = ToastNotifier()
                toaster.show_toast("Someone Is Online",
                                "Terminating Game",
                                duration=10)

            else:

                # Notify
                notify2.init("Roblox Notifier")
                notice = notify2.Notification("Roblox Notifier", "Someone Is Online")
                notice.show()

    else:
        # Reset once no one is online
        shouldnotify = True

    sleep(2)
