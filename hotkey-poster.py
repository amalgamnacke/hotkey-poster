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
            keyboard.add_hotkey(hotkey, self.playSoundById, [soundFileId])

    def start(self):
        # Block program from shutting down.
        keyboard.wait(self.config["shutdownhotkey"])

    def playSoundById(self, soundFileId):
        print("Requesting sound '{}' to play.".format(soundFileId))

        # Prepare URL.
        url = self.config["baseurl"] + self.config["uriplaysoundbyid"] + "/" + soundFileId

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

            req = urllib.request.Request(url)
            resp = opener.open(req)
        else:
            req = request.Request(url)
            resp = request.urlopen(req)

a = HotkeyPoster()
a.start()
