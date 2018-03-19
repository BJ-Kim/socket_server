# -*- coding: utf-8 -*-
import sys
from socket import *
from threading import Thread
import threading
import SocketServer

# class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
#     def handle(self):
#         while True:
#             data = self.request.recv(1024)
#             print data
#             cur_thread = threading.current_thread()
#             response = bytes("{}: {}".format(cur_thread.name, data))
#             self.request.sendall(response)
# 
# class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
#     pass
# userarr = []
# 
# def tcpHandler():
#     conn, addr = sock.accept()
#     print addr, "is connected"
#     testarr = []
#     while True:
#         data = conn.recv(1024)
#         if not data:
#             break
#         print "Receive", repr(data)
#         testarr.append(data)
#         userarr.append(data)
#         print testarr
#         print userarr

def accept_incoming_connections():
    while True:
        client, client_address = sock.accept()
        print client_address, "is connected"
        curr_thread = threading.current_thread()
        print curr_thread.name
        client.send(bytes("entered"))
        addresses[client] = client_address
        CLIENT_THREAD = Thread(target=handle_client, args=(client,))
        CLIENT_THREAD.setDaemon(True)
        CLIENT_THREAD.start()


def handle_client(client):
    name = client.recv(1024).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg))
    clients[client] = name
    curr_thread = threading.current_thread()
    print curr_thread.name

    while True:
        try:
            msg = client.recv(1024)
        except Exception as err:
            if err.errno == 54:
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % name))
                break
        else:
            if msg != bytes("{quit}") and len(msg) != 0:
                broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % name))
                break

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix)+msg)

class AcceptConnection (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            client, client_address = sock.accept()
            print client_address, "is connected"
            curr_thread = threading.current_thread()
            print curr_thread.name
            client.send(bytes("entered"))
            addresses[client] = client_address
            CLIENT_THREAD = Thread(target=handle_client, args=(client,))
            CLIENT_THREAD.setDaemon(True)
            CLIENT_THREAD.start()



clients = {}
addresses = {}

if __name__ == "__main__":
    HOST, PORT = "localhost", 1199

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(3)

    print "waiting connection"

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    # ACCEPT_THREAD2 = Thread(target=accept_incoming_connections)

    # ACCEPT_THREAD.start()
    # ACCEPT_THREAD.join()
    # sock.close()

    try:
        ACCEPT_THREAD.setDaemon(True)
        ACCEPT_THREAD.start()
        # ACCEPT_THREAD2.setDaemon(True)
        # ACCEPT_THREAD2.start()

        # ACCEPT_THREAD.join()
        while True:
            pass
    except KeyboardInterrupt:
        ACCEPT_THREAD._Thread__stop()
        sock.close()
        sys.exit(0)


    # for i in range(3):
    #     Thread(target=tcpHandler).start()

    # server = ThreadedTCPServer( (HOST, PORT), ThreadedTCPRequestHandler)
    # ip, port = server.server_address

    # server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.daemon = True
    # server_thread.start()

    # while True:
    #     pass
