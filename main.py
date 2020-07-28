import tkinter as tk
import threading
import socket
import time


def main():
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Project by: Roni, Gad, Elad and Bar")

    pack_tkinter_buttons(root)
    root.mainloop()


def pack_tkinter_buttons(root):
    button_1 = tk.Button(root, text='TCP Server', width=40, command=tcp_server_thread_handler)
    button_2 = tk.Button(root, text='TCP Client', width=40, command=tcp_client_thread_handler)
    button_close = tk.Button(root, text='Close', width=40, command=root.destroy)
    button_1.pack()
    button_2.pack()
    button_close.pack()


def tcp_server_thread_handler():
    # TODO put try catch, and close socket if close is pressed in UI
    tcp_server_thread = threading.Thread(target=tcp_server)
    if tcp_server_thread.is_alive():
        print("already alive")
    else:
        tcp_server_thread.start()


def tcp_client_thread_handler():
    # TODO put try catch, and close pocket if close is pressed in UI
    tcp_client_thread = threading.Thread(target=tcp_client)
    if tcp_client_thread.is_alive():
        print("already alive")
    else:
        tcp_client_thread.start()


def tcp_server():
    # socket info
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999

    server_socket.bind((host, port))
    # queue up to 5 requests
    server_socket.listen(5)

    client_socket, addr = server_socket.accept()
    print("Got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    client_socket.send(currentTime.encode('ascii'))
    client_socket.close()


def tcp_client():
    # client.py
    import socket

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    port = 9999

    # connection to hostname on the port.
    s.connect((host, port))

    # Receive no more than 1024 bytes
    tm = s.recv(1024)

    s.close()

    print("The time got from the server is %s" % tm.decode('ascii'))


if __name__ == "__main__":
    main()
