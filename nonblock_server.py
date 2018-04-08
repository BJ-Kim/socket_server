# -*- coding: utf-8 -*-
import time
import select, socket, sys, queue
from singletonClasses.connectInfo import ConnectionDatas

class SocketHandler:
    def __init__(self):
        self.connectData = ConnectionDatas.instance()
        self.outputs = []
        self.message_queues = {}

    def run(self):
        while self.connectData.connection_list:
            readable, writable, exceptional = select.select(self.connectData.connection_list, 
                                                            self.outputs, 
                                                            self.connectData.connection_list)
            for s in readable:
                if s is server:
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    # inputs.append(connection)
                    self.connectData.clientAdd(connection, None)
                    # print inputs
                    self.message_queues[connection] = Queue.Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        self.message_queues[s].put(data)
                        if s not in self.outputs:
                            self.outputs.append(s)
                    else:
                        if s in self.outputs:
                            self.outputs.remove(s)
                        # inputs.remove(s)
                        self.connectData.clientOut(s)
                        s.close()
                        del self.message_queues[s]
        
            for s in writable:
                try:
                    next_msg = self.message_queues[s].get_nowait()
                    if s in self.outputs:
                        self.outputs.remove(s)
                except Queue.Empty:
                    if s in self.outputs:
                        self.outputs.remove(s)
                except KeyError as keyErr:
                    print("key error")
                else:
                    a = 1 
                    del a
                    print(next_msg)
                    # s.send(next_msg)
        
            for s in exceptional:
                print("exception")
                # inputs.remove(s)
                self.connectData.clientOut(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_queues[s]

if __name__ == "__main__":
    HOST, PORT = "localhost", 1198
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind((HOST, PORT))
    server.listen(5)

    # inputs = [server]
    # outputs = []
    # message_queues = {}

    connectData = ConnectionDatas.instance()
    connectData.clientAdd(server,None)

    socketHandler = SocketHandler()
    socketHandler.run()
