# -*- coding: utf-8 -*-
import time
import select, socket, sys, Queue
from singletonClasses.connectInfo import ConnectionDatas

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(0)
# server.bind(('localhost', 1198))
# server.listen(5)
# inputs = [server]
# outputs = []
# message_queues = {}
# 
# while inputs:
#     # readable, writable, exceptional = select.select(inputs, outputs, inputs)
#     readable, writable, exceptional = select.select(inputs, outputs, inputs)
#     for s in readable:
#         if s is server:
#             connection, client_address = s.accept()
#             connection.setblocking(0)
#             inputs.append(connection)
#             message_queues[connection] = Queue.Queue()
#         else:
#             data = s.recv(1024)
#             if data:
#                 message_queues[s].put(data)
#                 if s not in outputs:
#                     outputs.append(s)
#             else:
#                 if s in outputs:
#                     outputs.remove(s)
#                 inputs.remove(s)
#                 s.close()
#                 del message_queues[s]
# 
#     for s in writable:
#         try:
#             next_msg = message_queues[s].get_nowait()
#         except Queue.Empty:
#             outputs.remove(s)
#         else:
#             print(next_msg)
#             # s.send(next_msg)
# 
#     for s in exceptional:
#         inputs.remove(s)
#         if s in outputs:
#             outputs.remove(s)
#         s.close()
#         del message_queues[s]

class SocketHandler:
    def __init__(self):
        print "init"

    def run(self):
        connectData = ConnectionDatas.instance()
        # while inputs:
        while connectData.connection_list:
            # readable, writable, exceptional = select.select(inputs, outputs, inputs)
            readable, writable, exceptional = select.select(connectData.connection_list, outputs, connectData.connection_list)
            for s in readable:
                if s is server:
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    # inputs.append(connection)
                    connectData.clientAdd(connection, None)
                    # print inputs
                    message_queues[connection] = Queue.Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        message_queues[s].put(data)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        # inputs.remove(s)
                        connectData.clientOut(s)
                        s.close()
                        del message_queues[s]
        
            for s in writable:
                try:
                    next_msg = message_queues[s].get_nowait()
                    # next_msg = message_queues[s].get()
                # except Queue.Empty:
                except:
                    if s in outputs:
                        outputs.remove(s)
                else:
                    # a = 1
                    # del a
                    print(next_msg)
                    # s.send(next_msg)
        
            for s in exceptional:
                # inputs.remove(s)
                connectData.clientOut(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del message_queues[s]

if __name__ == "__main__":
    HOST, PORT = "localhost", 1198
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.bind((HOST, PORT))
    server.listen(5)

    inputs = [server]
    outputs = []
    message_queues = {}

    connectData = ConnectionDatas.instance()
    connectData.clientAdd(server,None)

    socketHandler = SocketHandler()
    socketHandler.run()
