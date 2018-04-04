import select
from socket import *
from singletonClasses.connectInfo import ConnectionDatas

# localIP     = "localhost"
# localPort   = 1198
# bufferSize  = 1024
# 
# msgFromServer       = "Hello UDP Client"
# bytesToSend         = str.encode(msgFromServer)
# 
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.bind((localIP, localPort))
# print localIP
# print localPort
# print("UDP server up and listening")
# connectData = ConnectionDatas.instance()
# 
# while(True):
#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#     message = bytesAddressPair[0]
#     address = bytesAddressPair[1]
#     connectData.clientAdd(address, None)
#     print connectData.connection_list
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP  = "Client IP Address:{}".format(address)
#     print(clientMsg)
#     print(clientIP)
#     UDPServerSocket.sendto(bytesToSend, address)

HOST, PORT = "localhost", 1198

tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(5)

udp = socket(AF_INET, SOCK_DGRAM)
udp.bind((HOST, PORT))

input = [tcp, udp]

while True:
    read, write, error = select.select(input, [], [])
    for s in read:
        print "--------------"
        print s == tcp
        print s == udp
        print "--------------"
        if s == tcp:
            print "tcp"
            client, addr = s.accept()
            data = client.recv(1024)
            print data
            
        elif s == udp:
            print "udp"
            data, addr = s.recvfrom(1024)
            print data
        else:
            print "etc"
            data = s.recv(1024)
            if data:
                print "new data good"
                print data
            else:
                # connection_list.remove(sock)
                s.close()
                print "bye user"
