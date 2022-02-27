
from lib.application import Application
from lib.system import System


def main():
    system = System.get_instance()
    system.start()

    app = Application()
    app.start()

    # waiting for application loop break

    app.stop()
    system.stop()


if __name__ == "__main__":
    main()
