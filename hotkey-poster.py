import keyboard
import configparser
from urllib import request, parse
        
class HotkeyPoster:
    """HotkeyPoster."""
    
    config = {}
    hoykeys = {}
    
    def __init__(self):
        # Read config file.
        configParser = configparser.ConfigParser()
        configParser.read("config.ini")

        self.config = dict(configParser.items("Config"))

        self.hotkeys = dict(configParser.items("Hotkeys"))
        self.registerHotkeys()

    def registerHotkeys(self):
        for hotkey, soundFileId in self.hotkeys.items():
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

        # Perform POST request.
        req = request.Request(url, data = payload)
        
        resp = request.urlopen(req)

a = HotkeyPoster()
a.start()
