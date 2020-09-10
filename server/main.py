import socket
import sys
import os
import ClientThread


USE_PORT = 32007  # TODO: remove this and allow user to choose his own port
BUFFER_SIZE = 1024
SOCKET_PATH = "chat.sock"  # TODO: same as above
BACKLOG_SIZE = 10

connected_clients = []


def main():
    args_num = len(sys.argv)
    if args_num < 2:
        print("You should run " + sys.argv[0] +
              " with the following command line parameters:\nTCP (IPv4/IPv6), UDP (IPv4/IPv6), UDS")
        return

    convert_list_to_lower_case(sys.argv)
    sock_type, sock_bind, sock_family, ip_addr = get_protocol_attributes()

    # create server socket
    server_socket = socket.socket(sock_family, sock_type)
    if sys.argv[1] == 'tcp':
        # prevent "Address already in use" exception because of TIME_WAIT state
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(sock_bind)
    if sys.argv[1] == 'tcp' or sys.argv[1] == 'uds':
        server_socket.listen(BACKLOG_SIZE)

    print("Server is listening for incoming connections")

    if sys.argv[1] == "uds":
        print("socket file path: " + sock_bind)
    else:
        print(ip_addr + ":" + str(USE_PORT) + " (" + sys.argv[1] + ")")

    while True:
        if sys.argv[1] == 'udp':
            # UDP protocol DO NOT listen to incoming messages, instead of socket.listen() we should just receive messages with socket.revcfrom()
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
        else:
            connection, clientIP = server_socket.accept()

        # TODO handle UDP connection based, as it's not possible to use the same logic as TCP/UDS uses

        connected_clients.append(connection)

        if sys.argv[1] == 'uds':
            print("client connected to this server " + str(len(connected_clients)) + " clients are connected)")
            ClientThread(connection, "")
        else:
            print("client " + clientIP[0] + " connected to this server (" + str(len(connected_clients)) + " clients are connected)")
            ClientThread(connection, clientIP[0])


def get_ip_addr(ipv, port):
    hostname = socket.gethostbyname(socket.gethostname())
    ip_info = socket.getaddrinfo(hostname, port, ipv)
    return ip_info[0][4][0]


def convert_list_to_lower_case(my_list):
    for i in range(len(my_list)):
        sys.argv[i] = str(sys.argv[i]).lower()


def get_protocol_attributes():
    # TCP/UDP based server
    if sys.argv[1] == 'tcp' or sys.argv[1] == 'udp':
        sock_type = socket.SOCK_STREAM if sys.argv[1] == "tcp" else socket.SOCK_DGRAM
        try:
            if sys.argv[2] != 'ipv4' and sys.argv[2] != 'ipv6':
                raise IndexError
            sock_family = socket.AF_INET if sys.argv[2] == 'ipv4' else socket.AF_INET6
        except IndexError:
            print("You must select IP version!\nPlease run: " + sys.argv[0] + " " + sys.argv[1] + " ipv4 or ipv6")

        ip_addr = get_ip_addr(sock_family, USE_PORT)
        sock_bind = (ip_addr, USE_PORT)

    # UDS based server
    elif sys.argv[1] == 'uds':
        # remove socket file if already exists
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            raise

        sock_family = socket.AF_UNIX
        sock_type = socket.SOCK_STREAM
        sock_bind = SOCKET_PATH

    else:
        print("selected protocol " + sys.argv[1] + " is NOT supported")

    return sock_type, sock_bind, sock_family, ip_addr


if __name__ == '__main__':
    main()
