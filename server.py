import socket
import select


HEADER_LEN = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = {}

clients_pos = {}

def receive_message(client_socket) -> bool | dict:
    try:
        message_header = client_socket.recv(HEADER_LEN)

        if not len(message_header):
            return False
        
        message_lenght = int(message_header.decode("utf-8").strip())
        return {"header": message_header,
                "data": client_socket.recv(message_lenght)}
    except:
        return False

while True:
    read_sockets, _, execption_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket is server_socket:
            client_socket, client_adress = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accepted new connection from {client_adress[0]}:{client_adress[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                del clients_pos[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            clients_pos[notified_socket] = message['data'].decode('utf-8')

            for client_socket in clients:
                if client_socket is not notified_socket: #? is not <=> !=
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    print(f"sending message {message['data'].decode('utf-8')} to {clients_pos[notified_socket]} to user: {clients[notified_socket]['data'].decode('utf-8')}")
                    client_socket.send(message['header'] + message['data'])
    
    for notified_socket in execption_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        del clients_pos[notified_socket]