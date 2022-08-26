# Copyright (C) 2022 JKinc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#    
# Please post bugs and suggestions on GitHub at https://github.com/JKincorperated/The-Roblox-Anti-Social-Tool
    
from time import sleep
import os
import configparser
import json
import sys
import requests
from colorama import init, Fore, Style
import notify2

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

os.chdir(application_path)

##
## Declare your UID below in quotes
##

config = configparser.ConfigParser()
config.read('shouldterminate.conf')

uid = str(config['DEFAULT']['userid'])


# Initialise Colorama
init()

# Clear function
def cls():
    os.system('cls')

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
            
            # Check if code should terminate game
            try:
                if str(config['DEFAULT']['autoterminate']) == "yes":
                    os.system("""start cmd /c "taskkill /f /IM RobloxPlayerBeta.exe" """)
            except FileNotFoundError:
                pass

            # Notify
            notify2.init("Roblox Notifier")
            notice = notify2.Notification("Roblox Notifier", "Someone Is Online")
            notice.show()


    else:
        # Reset once no one is online
        shouldnotify = True

    sleep(2)

