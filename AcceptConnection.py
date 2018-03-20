# -*- coding: utf-8 -*-
from threading import Thread
import threading
from singletonClasses.serverConnectInfo import SingletonDatas
from handlerClasses.client_handler import ClientHandler

class AcceptConnection (threading.Thread):
    def __init__(self, sock):
        self.sock = sock
        threading.Thread.__init__(self)

    def broadcast(self, msg, prefix=""):
        singleDatas = SingletonDatas.instance()
        for sock in singleDatas.clients:
            sock.send(bytes(prefix)+msg)

    def run(self):
        while True:
            print 111
            client, client_address = self.sock.accept()

            print client_address, "is connected"

            curr_thread = threading.current_thread()
            print curr_thread.name

            client.send(bytes("entered"))

            CLIENT_THREAD = ClientHandler(client)
            CLIENT_THREAD.setDaemon(True)
            CLIENT_THREAD.start()

            # name = client.recv(1024).decode("utf8")

            # welcomeStr = "Welcome %s!" % name
            # client.send(bytes(welcomeStr))
            # msg = "%s has joined the chat!" % name
            # self.broadcast(bytes(msg))

            # singleDatas = SingletonDatas.instance()
            # singleDatas.clientAdd(client, name)
            # print singleDatas.clients

