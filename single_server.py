# -*- coding: utf-8 -*-
import sys
from socket import *
from threading import Thread
import threading
import SocketServer
import select
from AcceptConnection import AcceptConnection
from singletonClasses.serverConnectInfo import SingletonDatas
from singletonClasses.connectInfo import ConnectionDatas

clients = {}
addresses = {}


class SocketHandler(threading.Thread):
    def __init__(self, sock):
        self.server_sock = sock
        threading.Thread.__init__(self)

    def run(self):
        # while connection_list:
        connectData = ConnectionDatas.instance()
        while connectData.connection_list:
            try:
                # read_socket, write_socket, error_socket = select.select(connection_list, [], [], 10)
                read_socket, write_socket, error_socket = select.select(connectData.connection_list, [], [], 10)
                curr_thread = threading.current_thread()
                print curr_thread.name

                for sock in read_socket:
                    if sock == self.server_sock:
                        clientSocket, addr_info = self.server_sock.accept()
                        # connection_list.append(clientSocket)
                        connectData.clientAdd(clientSocket, None)
                        print "new user"

                        # for socket_in_list in connection_list:
                        for socket_in_list in connectData.connection_list:
                            if socket_in_list != self.server_sock and socket_in_list != sock:
                                try:
                                    socket_in_list.send('here comes new challanger')
                                except Exception as e:
                                    socket_in_list.close()
                                    # connection_list.remove(socket_in_list)
                                    connectData.clientOut(socket_in_list)
                    else:
                        data = sock.recv(1024)
                        if data:
                            print "new data good"
                            print data
                        else:
                            # connection_list.remove(sock)
                            connectData.clientOut(sock)
                            sock.close()
                            print "bye user"
            except KeyboardInterrupt:
                self.server_sock.close()
                sys.exit()

if __name__ == "__main__":
    HOST, PORT = "localhost", 1198

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen(3)

    print "waiting connection"
    connection_list = [server_sock]
    connectData = ConnectionDatas.instance()
    connectData.clientAdd(server_sock,None)

    SERVER_THREAD = SocketHandler(server_sock)
    # SERVER_THREAD2 = SocketHandler(server_sock)
    # SERVER_THREAD3 = SocketHandler(server_sock)
    try:
        SERVER_THREAD.setDaemon(True)
        # SERVER_THREAD2.setDaemon(True)
        # SERVER_THREAD3.setDaemon(True)
        SERVER_THREAD.start()
        # SERVER_THREAD2.start()
        # SERVER_THREAD3.start()
        SERVER_THREAD.join()
        # SERVER_THREAD2.join()
        # SERVER_THREAD3.join()
    except KeyboardInterrupt:
        SERVER_THREAD._Thread__stop()
        sock.close()
        sys.exit(0)


