
from time import sleep


class Backend:
    def __init__(self):
        self.handler = None

    def start(self):
        pass

    def stop(self):
        pass

    def register_handler(self, handler):
        self.handler = handler

    def send_out_message(self, out_message):
        pass
        # =====================
        # === short circuit ===
        # =====================
        sleep(0.28)
        dummy = out_message[::-1]
        result = self.handle_in_message(dummy)
        # =====================
        return "OK"

    def handle_in_message(self, in_message):
        result = self.handler(in_message)
        return result
