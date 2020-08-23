from threading import *
import select
import time


class Chat(Thread):

    def __init__(self, connection, client_address):
        Thread.__init__(self)
        self.id = None
        self.chat_history = None
        self.connection = connection
        self.client_address = client_address
        self.start()

    def run(self):
        self.connection.setblocking(0)
        time.sleep(1)
        while 1:
            ready = select.select([self.connection], [], [], 900)
            if ready[0]:
                data = self.connection.recv(1024).decode()
                print('Client connected to chat:', data)
                self.connection.send(b"Connection made to chat: " + data.encode())

    def create_new_chat(self, new_id):
        self.id = new_id
