import socket
import sys
import os
from Chat import Chat

def main():
    # some constants
    USE_PORT        = 32007
    SOCKET_PATH     = "chat.sock"
    BACKLOG_SIZE    = 10

    # Dealing with command line arguments
    argsNum = len(sys.argv)
    if argsNum < 2:
        print("You should run " + sys.argv[0] +
              " with the following command line parameters:\nTCP (IPv4/IPv6), UDP (IPv4/IPv6), UDS")
        return

    # convert all arguments to lower-case
    for i in range(0, argsNum):
        sys.argv[i] = str(sys.argv[i]).lower()

    # TCP based server
    if sys.argv[1] == 'tcp':
        ipv = IPversion()
        if ipv is False:
            return

        if ipv == 4:
            useType = socket.AF_INET
        else:
            useType = socket.AF_INET6

        ipaddr = getIPaddr(useType, USE_PORT)

        # create socket
        server_socket = socket.socket(useType, socket.SOCK_STREAM)
        server_socket.bind((ipaddr, USE_PORT))
        server_socket.listen(BACKLOG_SIZE)

        print("Server is listening for incoming connections, " + ipaddr + ":" + str(USE_PORT) + " (TCP)")

        while True:
            connection, client_address = server_socket.accept()
            Chat(connection, client_address)

    # UDP based server
    elif sys.argv[1] == 'udp':
        ipv = IPversion()
        if ipv is False:
            return

        if ipv == 4:
            useType = socket.AF_INET
        else:
            useType = socket.AF_INET6

        ipaddr = getIPaddr(useType, USE_PORT)

        # create socket
        server_socket = socket.socket(useType, socket.SOCK_DGRAM)
        server_socket.bind((ipaddr, USE_PORT))

        print("Server is listening for incoming connections, " + ipaddr + ":" + str(USE_PORT) + " (UDP)")

        # FYI
        # UDP protocol DO NOT listen to incoming messages, instead of socket.listen() we should just receive messages with socket.revcfrom()
        while True:
            data, addr = server_socket.recvfrom(1024) # 1024 is selected buffer size
            print("message: " + data + " from: " + addr)

    # UDS based server
    elif sys.argv[1] == 'uds':
        # create socket

        # remove socket file if already exists
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            raise

        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.bind(SOCKET_PATH)
        server_socket.listen(BACKLOG_SIZE)

        print("Server is listening for incoming connections, " + str(SOCKET_PATH) + " (UDS)")

        while True:
            connection, client_address = server_socket.accept()
            Chat(connection, client_address)

    else:
        print("selected protocol " + sys.argv[1] + " is NOT supported")
        return

def IPversion():
    try:
        if sys.argv[2] == 'ipv4':
            return 4

        if sys.argv[2] == 'ipv6':
            return 6
    except IndexError:
        print("You should select IP version!\nPlease run: " + sys.argv[0] + " " + sys.argv[1] + " ipv4 or ipv6")
        return False

def getIPaddr(ipv, port):
    hostname = socket.getfqdn()
    ipinfo = socket.getaddrinfo(hostname, port, ipv)
    return ipinfo[0][4][0]

if __name__ == '__main__':
    main()
