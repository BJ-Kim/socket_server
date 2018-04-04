# -*- coding: utf-8 -*-
import socket
import threading

ip, port = "localhost", 1198

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print ip
    print port
    # aa = input("message:")
    # sock.sendto(bytes(aa), (ip, port))
    while True:
        aa = raw_input("message:")
        sock.sendto(bytes(aa), (ip, port))
        # fromServer = sock.recvfrom(1024)
        # print fromServer
