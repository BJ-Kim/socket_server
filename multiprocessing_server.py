# -*- coding: utf-8 -*-
import sys
from socket import *
from threading import Thread
from multiprocessing import Process, Queue
import multiprocessing
import threading
import SocketServer
import select
from AcceptConnection import AcceptConnection
from singletonClasses.serverConnectInfo import SingletonDatas
from singletonClasses.connectInfo import ConnectionDatas

clients = {}
addresses = {}


class SocketHandler(Process):
    def __init__(self, sock):
        super(SocketHandler, self).__init__()
        self.server_sock = sock
        if not shared_state:
            with shared_state_lock:
                shared_state['x'] = 1
        else:
            print("already initalizedd")
        # threading.Thread.__init__(self)

    def run(self):
        # connectData = ConnectionDatas.instance()
        with shared_state_lock:
            print shared_state['connection']
            connectData = shared_state['connection_data']
        while connectData.connection_list:
            try:
                # read_socket, write_socket, error_socket = select.select(connection_list, [], [], 10)
                read_socket, write_socket, error_socket = select.select(connectData.connection_list, [], [], 10)
                # curr_thread = threading.current_thread()
                # print curr_thread.name
                curr_process = multiprocessing.current_process()
                print curr_process.name

                for sock in read_socket:
                    if sock == self.server_sock:
                        clientSocket, addr_info = self.server_sock.accept()
                        # connection_list.append(clientSocket)
                        connectData.clientAdd(clientSocket, None)

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
                            # print data
                        else:
                            # connection_list.remove(sock)
                            connectData.clientOut(sock)
                            sock.close()
                            # print "bye user"
            except KeyboardInterrupt:
                self.server_sock.close()
                sys.exit()

if __name__ == "__main__":
    HOST, PORT = "localhost", 1198

    shared_state = multiprocessing.Manager().dict()
    shared_state_lock = multiprocessing.Lock()

    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen(3)

    print "waiting connection"
    connection_list = [server_sock]
    connectData = ConnectionDatas.instance()
    connectData.clientAdd(server_sock,None)
    # with shared_state_lock:
    #     shared_state['connection_data'] = connectData
    #     shared_state['connection'] = {}

    # SERVER_THREAD = SocketHandler(server_sock)
    # SERVER_THREAD2 = SocketHandler(server_sock)
    # SERVER_THREAD3 = SocketHandler(server_sock)
    SERVER_PROCESS = SocketHandler(server_sock)
    SERVER_PROCESS2 = SocketHandler(server_sock)
    try:
        # SERVER_THREAD.setDaemon(True)
        # SERVER_THREAD2.setDaemon(True)
        # SERVER_THREAD3.setDaemon(True)
        SERVER_PROCESS.daemon = True
        SERVER_PROCESS2.daemon = True
        # SERVER_THREAD.start()
        # SERVER_THREAD2.start()
        # SERVER_THREAD3.start()
        SERVER_PROCESS.start()
        SERVER_PROCESS2.start()
        # SERVER_THREAD.join()
        # SERVER_THREAD2.join()
        # SERVER_THREAD3.join()
        SERVER_PROCESS.join()
        SERVER_PROCESS2.join()
    except KeyboardInterrupt:
        SERVER_PROCESS.terminate()
        SERVER_PROCESS2.terminate()
        # SERVER_THREAD._Thread__stop()
        server_sock.close()
        sys.exit(0)


