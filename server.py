# -*- coding: utf-8 -*-
import sys
from socket import *
from threading import Thread
import threading
import SocketServer
from AcceptConnection import AcceptConnection
from singletonClasses.serverConnectInfo import SingletonDatas

clients = {}
addresses = {}

if __name__ == "__main__":
    HOST, PORT = "localhost", 1198

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(3)

    print "waiting connection"

    SERVER_THREAD = AcceptConnection(sock)

    try:
        SERVER_THREAD.setDaemon(True)
        SERVER_THREAD.start()
        # SERVER_THREAD.join()
        while True:
            pass
    except KeyboardInterrupt:
        SERVER_THREAD._Thread__stop()
        sock.close()
        sys.exit(0)
