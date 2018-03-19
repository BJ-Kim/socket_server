# -*- coding: utf-8 -*-
from threading import Thread
import threading
from singletonClasses.serverConnectInfo import SingletonDatas
from handlerClasses.client_handler import ClientHandler

class AcceptConnection (threading.Thread):
    def __init__(self, sock):
        self.sock = sock
        threading.Thread.__init__(self)

    def run(self):
        while True:
            client, client_address = self.sock.accept()
            print client_address, "is connected"
            curr_thread = threading.current_thread()
            print curr_thread.name
            client.send(bytes("entered"))
            # addresses[client] = client_address

            CLIENT_THREAD = ClientHandler(client)
            CLIENT_THREAD.setDaemon(True)
            CLIENT_THREAD.start()

            #CLIENT_THREAD = Thread(target=handle_client, args=(client, ))
            #CLIENT_THREAD.setDaemon(True)
            #CLIENT_THREAD.start()
