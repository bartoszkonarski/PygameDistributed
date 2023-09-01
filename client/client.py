import socket
import json

from client.network_settings import CONFIG
class Network:

    def __init__(self, zone_name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = CONFIG[zone_name]['server']
        self.port = CONFIG[zone_name]['port']
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
            return json.loads(reply)
        except socket.error as e:
            return str(e)