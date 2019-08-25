import keyboard
import configparser
from urllib import request, parse

import urllib.request
import urllib.response
        
class HotkeyPoster:
    """HotkeyPoster."""
    
    config = {}
    hoykeys = {}
    
    def __init__(self):
        # Read config file.
        configParser = configparser.ConfigParser(delimiters=("="))
        configParser.read("config.ini")

        self.config = dict(configParser.items("Config"))

        self.hotkeys = dict(configParser.items("Hotkeys"))
        self.registerHotkeys()

    def registerHotkeys(self):
        for hotkey, soundFileId in self.hotkeys.items():
            print("Registering hotkey '{}' for sound '{}'.".format(hotkey, soundFileId))
            keyboard.add_hotkey(hotkey, self.playSoundById, args=(self.config["username"], soundFileId))

    def start(self):
        # Block program from shutting down.
        keyboard.wait(self.config["shutdownhotkey"])

    def playSoundById(self, username, soundFileId):
        print("Requesting sound '{}' to play.".format(soundFileId))
        
        # Prepare payload.
        payload = parse.urlencode({"username": username, "soundFileId" : soundFileId}).encode()

        # Prepare URL.
        url = self.config["baseurl"] + self.config["uriplaysoundbyid"]

        # Prepare auth.
        authUsername = self.config["authusername"]
        authPassword = self.config["authpassword"]
        
        # Perform POST request.
        if self.config["addauthheaders"] == "true":
            passwordManager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            passwordManager.add_password(None, url, authUsername, authPassword)
            
            authHandler = urllib.request.HTTPBasicAuthHandler(passwordManager)

            opener = urllib.request.build_opener(authHandler)
            urllib.request.install_opener(opener)
            
            req = urllib.request.Request(url, data = payload)
            resp = opener.open(req)
        else:
            req = request.Request(url, data = payload)
            resp = request.urlopen(req)

a = HotkeyPoster()
a.start()
