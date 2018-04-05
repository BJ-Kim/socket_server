# -*- coding: utf-8 -*-
import socket
import uuid
import time
import threading

ip, port = "localhost", 1198
# ip, port = "localhost", 5010

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    # sock.sendall(bytes("hello"))
    while True:
        try:
            # aa = raw_input("message:")
            # sock.sendall(bytes(aa))
            
            ran = uuid.uuid4()
            sock.sendall(bytes(ran))
            time.sleep(0.0001)

            # msg = str(sock.recv(1024))
            # print msg
        except OSError:
            break
    # response = str(sock.recv(1024))
    # print("Received: {}".format(response))
    sock.close()

