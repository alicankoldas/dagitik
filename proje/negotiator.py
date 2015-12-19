__author__ = 'AKOLDAS'


import socket
import threading
import select
import time
import datetime
import Queue


class Chat_Server(threading.Thread):
            def __init__(self,name,cSocket, addr,queue):
                threading.Thread.__init__(self)
                self.name = name
                self.cSocket = cSocket
                self.addr = addr
                self.queue = queue
                self.peer_ip = ""
                self.peer_port = ""
                self.connect_point = {}
            def run(self):
                while  True:
                        message = self.cSocket.recv(1024)
                        if message:
                            print "Daniel: " + message + ' (' + datetime.datetime.now().strftime('%H:%M:%S') + ')'
                            self.queue.put(message)



class Chat_Client(threading.Thread):
            def __init__(self,name,queue):
                threading.Thread.__init__(self)
                self.name = name
                self.queue = queue
                self.peer_ip = "127.0.0.1"
                self.peer_port = 12345
            def run(self):
                print "deneme"
                while  True:
                        if self.queue.qsize > 0 :
                                    data = self.queue.get()
                                    print "Maniel: " + data + ' (' + datetime.datetime.now().strftime('%H:%M:%S') + ')'
                                    try:
                                        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        sock.connect((self.peer_ip,  self.peer_port))
                                    except socket.error as e :
                                        print "hata var"
                                    self.cSocket.send("sunucunun ese cevabi")




queue = Queue.Queue()
client_read = Chat_Client("ClientThread ",queue)
client_read.start()
#negotiator server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 12345
s.bind((host,port))
s.listen(5)
threadCounter = 0
while True :
    c,addr = s.accept()
    print "Got a connection from", addr
    threadCounter += 1
    thread = Chat_Server("ChatServer",c,addr,queue)
    thread.start()