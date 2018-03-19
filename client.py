# -*- coding: utf-8 -*-
import socket
import threading

ip, port = "localhost", 1198

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(bytes("hello"))
    while True:
        try:
            msg = str(sock.recv(1024))
            print msg
        except OSError:
            break
    # response = str(sock.recv(1024))
    # print("Received: {}".format(response))
    sock.close()

