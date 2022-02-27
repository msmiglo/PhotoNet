
from lib.backend import Backend
from lib.frontend import Frontend


class Application:
    def __init__(self):
        self.backend = Backend()
        self.frontend = Frontend(self.backend)

    def start(self):
        self.backend.start()
        self.frontend.start()

    def stop(self):
        self.frontend.stop()
        self.backend.stop()
