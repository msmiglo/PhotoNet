
from random import randint
import socket
from threading import Lock
import uuid

from lib.driver import PhotoNetDriver
from lib.ethernet import Ethernet
from lib.ip_service import IpService
from lib.tcp_socket import _BaseSocket


DYNAMIC_PORT_MIN = 49152
DYNAMIC_PORT_MAX = 65535


class System:
    """ Implements singleton design pattern. """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.initiate()
        return cls._instance

    def __init__(self):
        raise NotImplementedError("Please use `get_instance` method.")

    def initiate(self):
        ip, mac = self.__get_addresses()
        self.ip = ip
        self.mac = mac
        self.arp = dict()
        self.registered_ports = dict()
        self.ports_lock = Lock()

        self.photo_driver = PhotoNetDriver()
        self.ethernet = Ethernet(mac_address=self.mac)
        self.ip_service = IpService(ip_address=self.ip)

    def start(self):
        self.photo_driver.start()
        self.ethernet.start()
        self.ip_service.start()

    def stop(self):
        for port, socket in self.registered_ports.items():
            socket.stop()

        self.ip_service.stop()
        self.ethernet.stop()
        self.photo_driver.stop()

    @staticmethod
    def __get_addresses():
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        mac = uuid.getnode()
        return ip, mac

    def show_free_port(self):
        random_port = randint(DYNAMIC_PORT_MIN, DYNAMIC_PORT_MAX)
        while random_port in self.registered_ports:
            random_port += 1
            if random_port > DYNAMIC_PORT_MAX:
                random_port = DYNAMIC_PORT_MIN
        return random_port

    def aquire_port(self, port, socket):
        self.ports_lock.aquire()
        assert isinstance(port, int)
        assert 0 < port < 2**16
        assert isinstance(socket, _BaseSocket)
        if port in self.registered_ports:
            raise RuntimeError(f"Port {port} is already in use.")
        self.registered_ports[port] = socket
        self.ports_lock.release()

    def release_port(self, port):
        self.ports_lock.aquire()
        if port not in self.registered_ports:
            raise RuntimeError(f"Port {port} has not been in use.")
        del self.registered_ports[port]
        self.ports_lock.release()
