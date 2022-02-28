
import json

from lib.backend import Backend
from lib.frontend import Frontend


CONFIG_PATH = "./config/config.json"


class Application:
    def __init__(self):
        config = json.load(open(CONFIG_PATH))
        self.backend = Backend(config)
        self.frontend = Frontend(self.backend)

    def start(self):
        self.backend.start()
        self.frontend.start()

    def stop(self):
        self.frontend.stop()
        self.backend.stop()
