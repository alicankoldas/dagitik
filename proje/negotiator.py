__author__ = 'AKOLDAS'


import socket
import threading
import select
import time
import datetime
import Queue

dict = {}

class Chat_Server(threading.Thread):
            def __init__(self,name,cSocket, addr,queue,fihrist):
                threading.Thread.__init__(self)
                self.name = name
                self.cSocket = cSocket
                self.addr = addr
                self.queue = queue
                self.fihrist = fihrist
                self.peer_ip = ""
                self.peer_port = ""
                self.connect_point = {}
            def run(self):
                while  True:
                        message = self.cSocket.recv(1024)
                        #message_1 = str(self.cSocket)
                        self.fihrist[message] = self.cSocket
                        print str(self.fihrist)
                        if message:
                            print "Daniel: " + message + ' (' + datetime.datetime.now().strftime('%H:%M:%S') + ')'
                            self.queue.put(message)


class Chat_Read_Client(threading.Thread):
            def __init__(self,name,msg_queue,sockk,fihrist):
                threading.Thread.__init__(self)
                self.name = name
                self.msg_queue = msg_queue
                self.sockk = sockk
                self.fihrist = fihrist
            def run(self):
                print "deneme_1"
                while True :
                        if self.msg_queue.qsize > 0 :
                                data_1 = self.msg_queue.get()
                                print data_1
                                data_2 = data_1.split(" ")
                                print "deneme_5"
                                print data_2[1]
                                for mess, sock in self.fihrist.iteritems() :
                                    print "deneme_2"
                                    if data_2[1] == mess :
                                        print "deneme_van"
                                        sock.send("OK")


                                #self.sockk.send(data_1)
                                #data_1 = data_1.split(" ")
                                #print data_1[1]+"merhaba"
                                #data_1[1].send(data_1[0])





class Chat_Client(threading.Thread):
            def __init__(self,name,queue,msg_queue):
                threading.Thread.__init__(self)
                self.name = name
                self.queue = queue
                self.msg_queue = msg_queue
                self.peer_ip = "127.0.0.1"
                self.peer_port = 12345
            def run(self):
                print "deneme"
                while  True:
                        if self.queue.qsize > 0 :
                                    data = self.queue.get()
                                    print "Maniel: " + data + ' (' + datetime.datetime.now().strftime('%H:%M:%S') + ')'
                                    try:
                                        client_Socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        client_Socket.connect((self.peer_ip,  self.peer_port))
                                    except socket.error as e:
                                            client_Socket.close()
                                    mesaj_1 = "cevabi"
                                    mesaj_2 = data
                                    mesaj_3 = mesaj_1+" "+mesaj_2
                                    self.msg_queue.put(mesaj_3)
                                    client_read = Chat_Read_Client("ClientThread ",msg_queue,client_Socket,dict)
                                    client_read.start()



queue = Queue.Queue()
msg_queue = Queue.Queue()
client=Chat_Client("Client",queue,msg_queue)
client.start()
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
    thread = Chat_Server("ChatServer",c,addr,queue,dict)
    thread.start()