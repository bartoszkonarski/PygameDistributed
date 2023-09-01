import socket
import json
from _thread import *
import sys

from servers_config import CONFIG

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

CONFIG = CONFIG[sys.argv[1]]
server, port = CONFIG['server'], CONFIG['port']

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection")

currentId = 0
players_base = {}

def threaded_client(conn):
    global currentId, players_base
    localId = currentId
    conn.send(str.encode(str(currentId)))
    currentId += 1
    while True:
        try:
            data = json.loads(conn.recv(2048).decode('utf-8'))
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + str(data))
                
                client_id = data['id']
                if client_id not in players_base:
                    players_base[client_id] = {}
                
                if data['event_type'] in ("movement", "get_positions"):
                    players_base[client_id]['position'] = data['position']
                
                print("Sending: " + str(players_base))

            conn.sendall(str.encode(json.dumps(players_base)))



            
        except Exception as e:
            print(e)
            break
    del players_base[str(localId)]
    print(f"Connection ({localId}) Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))