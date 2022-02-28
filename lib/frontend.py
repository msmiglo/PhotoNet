
import os
from threading import Thread


CHANGE_TO_GREEN = "\033[92m"
CHANGE_TO_BLUE = "\033[94m"
CHANGE_TO_RED = "\033[91m"
RESET_COLOR = "\033[0m"


class Frontend:
    def __init__(self, backend):
        self.backend = backend
        self.backend.register_handle_callback(self.handle_in_message)
        self.is_connected = False

    def start(self):
        """ Start and run blocking loop. """
        # configure output
        os.system('color')
        print(f"Welcome to Internet communicator!")
        print()

        # wait for backend connection to other user...
        print("Waiting for connection...")
        #self.backend_ref.connected_user_event.wait()
        # TODO TODO TODO TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO TODO TODO TODO
        self.is_connected = True
        print("Found other connected user!")
        print()

        # show instructions
        print('Please enter the messages to send.')
        print(f'Your messages are in {CHANGE_TO_GREEN}green{RESET_COLOR},'
              f' their messages are in {CHANGE_TO_BLUE}blue{RESET_COLOR}.')
        print(f'Type "exit()" to  disconnect and end conversation.')
        print("=========================================================")

        # run loop
        while self.is_connected:
            message = self._read_input()
            if message == "exit()":
                break
            t = Thread(target=self.handle_out_message, args=(message,))
            t.start()
            # TODO - MAYBE IGNORE INPUTS WHEN THERE ARE TOO MANY ACTIVE THREADS

        # end communication
        print("=========================================================")
        print("Connection ended.")

    def stop(self):
        self.is_connected = False

    def _read_input(self):
        return input()

    def handle_in_message(self, message):
        print(CHANGE_TO_BLUE + "They: " + message + RESET_COLOR, flush=True)
        return "success"

    def handle_out_message(self, message):
        response = self.backend.send_out_message(message)
        if response == "success":
            print(CHANGE_TO_GREEN + "You: " + message + RESET_COLOR, flush=True)
        else:
            print(
                CHANGE_TO_RED + "Problem with sending message." + RESET_COLOR,
                flush=True
            )

    def __del__(self):
        print(RESET_COLOR, end="")
