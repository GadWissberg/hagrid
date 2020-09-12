import socket
import select
import sys

USE_PORT = 32007
BUFFER_SIZE = 1024


def main():
    protocol = input("Please choose protocol (TCP / UDP / UDS): ").lower()
    if protocol == "tcp" or protocol == "udp":
        sock_family = socket.AF_INET
        sock_type = socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM
        host = get_server_ip()
        if ":" in host:
            sock_family = socket.AF_INET6
    elif protocol == "uds":
        sock_family = socket.AF_UNIX
        sock_type = socket.SOCK_STREAM
        sock_file = input("Please insert path to server socket file: ")
    else:
        print("Unknown protocol")
        return

    try:
        server = socket.socket(sock_family, sock_type)
        if protocol == "uds":
            print("UDS: connecting to " + sock_file)
            server.connect(sock_file)
        else:
            print("connecting to " + host + ":" + str(USE_PORT))
            server.connect((host, USE_PORT))

    except Exception as e:
        print("Can't connect to server, please make sure that:\n"
              "1. server is running\n"
              "2. you have provided right connection information")

        print("Exception: "+str(e))
        return


    # list of available input streams
    streams = [sys.stdin, server]

    # TODO:
    # allow client to choose his own nickname
    #name = input("Enter your name: ")

    while True:
        readSock, writeSock, errSock = select.select(streams, [], [])
        for sock in readSock:
            if sock == server:
                # message received from server -> print to client
                message = sock.recv(BUFFER_SIZE)
                print(message.decode())
            else:
                # input from client -> send to server
                message = sys.stdin.readline()
                server.send(message.encode())
                print("<You> "+message)


def get_server_ip():
    host = input("Please insert server IP address (click enter for local host address): ")
    if host == "":
        host = socket.gethostbyname(socket.gethostname())
    return host


if __name__ == '__main__':
    main()
