


class HttpServer:
    def __init__(self, listener_port, handle_callback):
        self.listener_port = listener_port
        self.handle_callback = handle_callback
        self.socket = None

    def start(self):
        pass

    def stop(self):
        pass
