import socket
from Chat import Chat


def main():
    # TCP based server
    server_socket = socket.socket()
    print(socket.gethostbyname(socket.gethostname()))
    server_socket.bind((socket.gethostbyname(socket.gethostname()), 32007))
    server_socket.listen()
    while True:
        connection, client_address = server_socket.accept()
        Chat(connection, client_address)


if __name__ == '__main__':
    main()
