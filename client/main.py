import socket
import select
import sys

# some constants
USE_PORT    = 32007
BUFFER_SIZE = 1024

def main():
    protocol = input("Please choose protocol (TCP / UDP / UDS): ").lower()
    if protocol == "tcp" or protocol == "udp":
        sockFamily = socket.AF_INET
        sockType = socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM
        host = input("Please insert server IP address: ")
        if ":" in host:
            sockFamily = socket.AF_INET6
        port = int(input("Please insert server port: "))
    elif protocol == "uds":
        sockFamily = socket.AF_UNIX
        sockType = socket.SOCK_STREAM
        sockFile = input("Please insert path to server socket file: ")
    else:
        print("Unknown protocol")
        return

    try:
        server = socket.socket(sockFamily, sockType)
        if protocol == "uds":
            print("UDS: connecting to "+sockFile)
            server.connect(sockFile)
        else:
            print("connecting to " + host + ":"+str(port))
            server.connect((host, port))

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

if __name__ == '__main__':
    main()
