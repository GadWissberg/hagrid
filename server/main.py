import socket
import sys
import os
from threading import *

# some constants
USE_PORT        = 32007 # TODO: remove this and allow user to choose his own port
BUFFER_SIZE     = 1024
SOCKET_PATH     = "chat.sock" # TODO: same as above
BACKLOG_SIZE    = 10

# global vars
clients = [] # list of all connected clients

def main():
    # Dealing with command line arguments
    argsNum = len(sys.argv)
    if argsNum < 2:
        print("You should run " + sys.argv[0] +
              " with the following command line parameters:\nTCP (IPv4/IPv6), UDP (IPv4/IPv6), UDS")
        return

    # convert all arguments to lower-case
    for i in range(0, argsNum):
        sys.argv[i] = str(sys.argv[i]).lower()

    # TCP/UDP based server
    if sys.argv[1] == 'tcp' or sys.argv[1] == 'udp':
        sockType = socket.SOCK_STREAM if sys.argv[1] == "tcp" else socket.SOCK_DGRAM

        try:
            if sys.argv[2] != 'ipv4' and sys.argv[2] != 'ipv6':
                print("You must select IP version!\nPlease run: " + sys.argv[0] + " " + sys.argv[1] + " ipv4 or ipv6")
                return False

            sockFamily = socket.AF_INET if sys.argv[2] == 'ipv4' else socket.AF_INET6
        except IndexError:
            print("You must select IP version!\nPlease run: " + sys.argv[0] + " " + sys.argv[1] + " ipv4 or ipv6")
            return False

        ipaddr = getIPaddr(sockFamily, USE_PORT)
        sockBind = (ipaddr, USE_PORT)

    # UDS based server
    elif sys.argv[1] == 'uds':
        # remove socket file if already exists
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            raise

        sockFamily = socket.AF_UNIX
        sockType = socket.SOCK_STREAM
        sockBind = SOCKET_PATH

    else:
        print("selected protocol " + sys.argv[1] + " is NOT supported")
        return

    # create server socket
    server_socket = socket.socket(sockFamily, sockType)

    if sys.argv[1] == 'tcp':
        # prevent "Address already in use" exception because of TIME_WAIT state
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(sockBind)

    if sys.argv[1] == 'tcp' or sys.argv[1] == 'uds':
        server_socket.listen(BACKLOG_SIZE)

    print("Server is listening for incoming connections")

    if sys.argv[1] == "uds":
        print("socket file path: "+sockBind)
    else:
        print(ipaddr + ":" + str(USE_PORT) + " (" + sys.argv[1] + ")")

    while True:
        if sys.argv[1] == 'udp':
            # UDP protocol DO NOT listen to incoming messages, instead of socket.listen() we should just receive messages with socket.revcfrom()
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
        else:
            connection, clientIP = server_socket.accept()

        # TODO:
        # handle UDP connection based, as it's not possible to use the same logic as TCP/UDS uses

        clients.append(connection)

        if sys.argv[1] == 'uds':
            print("client connected to this server " + str(len(clients)) + " clients are connected)")
            clientThread(connection, "")
        else:
            print("client " + clientIP[0] + " connected to this server (" + str(len(clients)) + " clients are connected)")
            clientThread(connection, clientIP[0])

def getIPaddr(ipv, port):
    hostname = socket.getfqdn()
    ipinfo = socket.getaddrinfo(hostname, port, ipv)
    return ipinfo[0][4][0]

def sendMessage(msg, srcClient, IP):
    # broadcast message to all available clients, except the one who send the message

    # TODO: fix this if condition (do not work)
    # msg type is "bytes" class
    if msg == "":
        return False

    # it's possible to print here (to server console) "received message XXX from client YYY"

    for client in clients:
        # do not send to source client
        if client != srcClient:
            try:
                msg = "<"+IP+"> "+msg.decode()
                msg = msg.encode()
                client.send(msg)
            except Exception as e:
                print("sendMessage Exception: "+str(e))
                client.close()
                dropConnection(client)

def dropConnection(client):
    # remove client from our clients list
    if client not in clients:
        return False

    print(type(client))
    print(client)
    print("client lost connection")
    return clients.remove(client)


class clientThread(Thread):
    def __init__(self, client, ipaddr):
        Thread.__init__(self)
        self.client = client
        self.ipaddr = ipaddr
        #self.name = "" TODO: add support for client name/nick
        self.start()

    def run(self):
        self.client.send(b"Welcome to chat server!")

        while True:
            try:
                message = self.client.recv(BUFFER_SIZE)
                sendMessage(message, self.client, self.ipaddr)
            except Exception as e:
                print("clientThread Exception: "+str(e))

                # TODO:
                # disconnect client (connection timed-out / aborted / something happened)
                # stop thread and handle everything else
                continue

if __name__ == '__main__':
    main()
