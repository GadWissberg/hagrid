import socket


def main():
    # TCP based client socket
    echoClient = socket.socket()
    echoClient.connect((socket.gethostbyname(socket.gethostname()), 32007))
    chat_id = input("Enter chat ID: ")
    echoClient.send(chat_id.encode())
    while True:
        msgReceived = echoClient.recv(1024)
        print("At client: %s" % msgReceived.decode())
        echoClient.send(input().encode())


if __name__ == '__main__':
    main()
