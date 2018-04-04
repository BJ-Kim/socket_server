from gevent import monkey
monkey.patch_all()
import random
import time
import string
import select
import multiprocessing
import threading
from gevent import socket
from gevent.pool import Pool
from gevent.server import StreamServer
from singletonClasses.connectInfo import ConnectionDatas

def handle_echo(sock, address):
    print "hihi"
    curr_thread = threading.current_thread()
    print curr_thread.name
    curr_process = multiprocessing.current_process()
    print curr_process.name

    connectData = ConnectionDatas.instance()

    # data = sock.recv(1024)
    # if data:
    #     sock.sendall(data)

    # while connectData.connection_list:
    #     connectData.clientAdd(sock, None)
    while True:
      data = sock.recv(1024)
      print data
      # time.sleep(3)
      if data:
          print data
          # sock.sendall(data)
      else:
          print None
          break;

    sock.shutdown(socket.SHUT_WR)
    sock.close()

sock = socket.socket()
sock.bind(('localhost', 1198))
sock.listen(500)
connectData = ConnectionDatas.instance()
connectData.clientAdd(sock,None)

print 1
pool = Pool(3)
server = StreamServer(sock, handle_echo, spawn=pool)

# server = StreamServer(sock, handle_echo)
print 2

server.serve_forever()
