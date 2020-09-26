import socket
import sys
import os
import platform
from threading import *

from FileAPI import FileAPI

USE_PORT = 32007
BUFFER_SIZE = 1024
SOCKET_PATH = "chat.sock"
BACKLOG_SIZE = 10

connected_clients = []


class ClientThread(Thread):
    def __init__(self, client, ipaddr):
        Thread.__init__(self)
        self.client = client
        self.ipaddr = ipaddr
        # self.name = "" TODO: add support for client name/nick
        self.start()

    def run(self):
        self.client.send(b"Welcome to chat server!")

        while True:
            try:
                chat_history_file_name = self.ipaddr.replace(".", "_") + ".txt"
                message = self.client.recv(BUFFER_SIZE)
                FileAPI.write_msg_into_history_file(message.decode(), chat_history_file_name)
                if message.decode() == 'get_history':
                    self.send_client_history()
                else:
                    self.send_message(message, self.client, self.ipaddr)
            except Exception as e:
                print("clientThread Exception: " + str(e))
                continue

    def send_message(self, msg, src_client, ip):
        """
        broadcast message to all available clients, except the one who send the message
        """

        # it's possible to print here (to server console) "received message XXX from client YYY"
        for client in connected_clients:
            if client != src_client:
                try:
                    msg = "<" + ip + "> " + msg.decode()
                    msg = msg.encode()
                    client.send(msg)
                except Exception as e:
                    print("sendMessage Exception: " + str(e))
                    client.close()
                    self.drop_connection(client)

    @staticmethod
    def drop_connection(client):
        # remove client from our clients list
        if client not in connected_clients:
            return False

        print(type(client))
        print(client)
        print("client lost connection")
        return connected_clients.remove(client)

    def send_client_history(self):
        try:
            msg = ("\n" + FileAPI.get_client_history).encode()
            self.client.send(msg)
        except Exception as e:
            print("sendMessage Exception: " + str(e))
            self.client.close()
            self.drop_connection(self.client)


def main():
    try:
        print("Welcome to Chat server!")
        print("\nRunning under the following system:")

        system_info = get_system_info()
        print("CPU:", system_info['cpu'],
              "\nMemory:", str(system_info['memory']['used']) + "GB", "used of", str(system_info['memory']['available']) +"GB total",
              "\nLoad average:", system_info['loadavg'][0], " 1 minute,", system_info['loadavg'][1], "5 minutes,", system_info['loadavg'][2], "15 minutes\n\n")

        # get protocol attributes by user selection and create proper socket
        sock_type, sock_bind, sock_family, ip_addr = get_protocol_attributes()
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
    except Exception as e:
        print(e)


def get_ip_addr(ipv, port):
    hostname = socket.gethostbyname(socket.gethostname())
    ip_info = socket.getaddrinfo(hostname, port, ipv)
    return ip_info[0][4][0]


def convert_list_to_lower_case(my_list):
    for i in range(len(my_list)):
        sys.argv[i] = str(sys.argv[i]).lower()


def get_protocol_attributes():
    args_num = len(sys.argv)
    if args_num < 2:
        raise Exception("You should run " + sys.argv[0] + " with the following command line parameters:\nTCP (IPv4/IPv6), UDP (IPv4/IPv6), UDS")
    convert_list_to_lower_case(sys.argv)

    if sys.argv[1] == 'tcp' or sys.argv[1] == 'udp':
        sock_type = socket.SOCK_STREAM if sys.argv[1] == "tcp" else socket.SOCK_DGRAM
        if sys.argv[2] != 'ipv4' and sys.argv[2] != 'ipv6':
            raise Exception("You must select IP version!\nPlease run: " + sys.argv[0] + " " + sys.argv[1] + " ipv4 or ipv6")
        sock_family = socket.AF_INET if sys.argv[2] == 'ipv4' else socket.AF_INET6

        ip_addr = get_ip_addr(sock_family, USE_PORT)
        sock_bind = (ip_addr, USE_PORT)
    elif sys.argv[1] == 'uds':
        # remove socket file if already exists
        try:
            os.unlink(SOCKET_PATH)
        except OSError:
            raise Exception("the path is a directory")

        sock_family = socket.AF_UNIX
        sock_type = socket.SOCK_STREAM
        sock_bind = SOCKET_PATH
    else:
        print("selected protocol " + sys.argv[1] + " is NOT supported")

    return sock_type, sock_bind, sock_family, ip_addr


def get_system_info():
    # get some system information from /proc file-system

    operating_system = platform.system()
    if operating_system != "Linux":
        raise Exception("You must run this application on a Linux machine. you are currently running it on: " + operating_system)

    with open("/proc/cpuinfo", "r") as f:
        cpuinfo = f.readlines()
        cpu = [cpu.strip().split(":")[1].strip() for cpu in cpuinfo if "model name" in cpu]
        cpu = cpu[0]  # get only 1st core

    # get memory info
    with open("/proc/meminfo", "r") as f:
        meminfo = f.readlines()
        free_ram = round(int(meminfo[1].split(":")[1].strip().split(" ")[0]) / 1024 / 1024, 2)  # free memory in GB
        avail_ram = round(int(meminfo[2].split(":")[1].strip().split(" ")[0])/1024/1024, 2)  # available memory in GB
        used_ram = round(avail_ram - free_ram, 2)

    # get system load average
    with open("/proc/loadavg", "r") as f:
        load = f.read().split(" ")
        load_1 = load[0]  # 1 min avg
        load_5 = load[1]  # 5 min avg
        load_15 = load[2]  # 15 min avg

    res = {
            "cpu": cpu,
            "memory": {"used": used_ram, "available": avail_ram, "free": free_ram},
            "loadavg": [load_1, load_5, load_15]
    }

    return res


if __name__ == '__main__':
    main()
