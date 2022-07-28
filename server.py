import socket
from _thread import *
import time

# host = '127.0.0.1'
host = socket.gethostname()
port = 1234
ThreadCount = 0
IDs = []

actions_arr = ["Absent", "Attending", "Hand raising", "Looking elsewhere", "Telephone call", "Using phone", "Writing"]

def client_handler(connection):
    data = connection.recv(2048)
    ID_message = data.decode('utf-8')
    # Insert a check to see if a student with that ID has already been connected
    if (ID_message in IDs):
        print(f"Student with ID {ID_message} already connected")
        connection.close()
    else:
        print(f"Student with ID: {ID_message}")
        IDs.append(ID_message)
    while True:
        data = connection.recv(2048)
        action_message = data.decode('utf-8')

        # Write the index of the most performed action in the text file
        # Note: indexing in Unity starts from 1 instead of 0
        max_index = actions_arr.index(action_message)
        print(f"Student with ID: {ID_message}, Performed action: {action_message}")
        with open(f'actions_{ID_message}.txt', 'w') as f:
            f.write(str(max_index + 1))


def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (Client, ))

def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)


start_server(host, port)