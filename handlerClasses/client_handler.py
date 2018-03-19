# -*- coding: utf-8 -*-
from threading import Thread
import threading
from singletonClasses.serverConnectInfo import SingletonDatas

class ClientHandler(threading.Thread):
    def __init__(self, client):
        self.client = client
        threading.Thread.__init__(self)

    def broadcast(self, msg, prefix=""):
        singleDatas = SingletonDatas.instance()
        for sock in singleDatas.clients:
            sock.send(bytes(prefix)+msg)

    def run(self):
        name = self.client.recv(1024).decode("utf8")
        welcomeStr = "Welcome %s!" % name
        self.client.send(bytes(welcomeStr))
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg))

        singleDatas = SingletonDatas.instance()
        singleDatas.clientAdd(self.client, name)
        print singleDatas.clients

        curr_thread = threading.current_thread()
        print curr_thread.name

        while True:
            try:
                msg = self.client.recv(1024)
            except Exception as err:
                if err.errno == 54:
                    self.client.send(bytes("{quit}"))
                    self.client.close()
                    singleDatas.clientOut(self.client)
                    print singleDatas.clients
                    self.broadcast(bytes("%s has left the chat." % name))
                    break
            else:
                if not msg:
                    self.client.send(bytes("{quit}"))
                    self.client.close()
                    singleDatas.clientOut(self.client)
                    print singleDatas.clients
                    self.broadcast(bytes("%s has left the chat." % name))
                    break
                else:
                    self.broadcast(msg, name+": ")
