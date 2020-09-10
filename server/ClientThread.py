from threading import *

BUFFER_SIZE = 1024
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
                message = self.client.recv(BUFFER_SIZE)
                self.send_message(message, self.client, self.ipaddr)
            except Exception as e:
                print("clientThread Exception: " + str(e))

                # TODO:
                # disconnect client (connection timed-out / aborted / something happened)
                # stop thread and handle everything else
                continue

    def send_message(self, msg, src_client, ip):
        # broadcast message to all available clients, except the one who send the message

        # TODO: fix this if condition (do not work)
        # msg type is "bytes" class
        if msg == "":
            return False

        # it's possible to print here (to server console) "received message XXX from client YYY"

        for client in connected_clients:
            # do not send to source client
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
