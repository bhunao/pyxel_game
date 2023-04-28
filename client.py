import socket
import select
import errno
import sys
import time
import logging


HEADER_LEN = 10
IP = "127.0.0.1"
PORT = 1234

class Client:
    def __init__(self, username) -> None:
        self.my_username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        self.client_socket.setblocking(False)

        self.username = self.my_username.encode("utf-8")
        self.username_header = f"{len(self.username):<{HEADER_LEN}}".encode('utf-8')
        self.client_socket.send(self.username_header + self.username)
    
    def send(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LEN}}".encode('utf-8')
        print(f"sending message: {message_header + message}")
        self.client_socket.send(message_header + message)
    
    def receive(self):
        username_header = self.client_socket.recv(HEADER_LEN)
        if not len(username_header):
            print("Connection closed by the server")
            sys.exit()
        
        username_length = int(username_header.decode('utf-8').strip())
        username = self.client_socket.recv(username_length).decode('utf-8')

        message_header = self.client_socket.recv(HEADER_LEN)
        message_length = int(message_header.decode('utf-8').strip())
        message = self.client_socket.recv(message_length).decode('utf-8')

        return username, message

    def connection(self):
        logging.debug("Starting connection")
        # message = self.my_username + str(time.time())
        # if message:
        #     self.send(message)
        
        try:
            while True:
                username, message = self.receive()
                print(f"{username} > {message}")
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno  != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
        except:
            pass

if __name__ == "__main__":
    client = Client("text")
    while True:
        client.connection()