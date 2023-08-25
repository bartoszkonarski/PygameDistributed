import socket
import json

from client.network_settings import IP_ADDRESS, PORT

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = IP_ADDRESS
        self.port = PORT
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data: dict) -> str:
        try:
            data_json = json.dumps(data)
            self.client.send(str.encode(data_json))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)