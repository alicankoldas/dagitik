__author__ = 'AKOLDAS'


import socket
import threading
import select
import time
import datetime
import Queue
from ast import literal_eval

dict = {}

class Chat_Server(threading.Thread):
            def __init__(self,name,cSocket, addr,queue,fihrist,msg_1_queue):
                threading.Thread.__init__(self)
                self.name = name
                self.cSocket = cSocket
                self.addr = addr
                self.queue = queue
                self.fihrist = fihrist
                self.msg_1_queue = msg_1_queue ;
                self.peer_ip = ""
                self.peer_port = ""
                self.control_value = ""
                self.connect_point = {}

            def parser(self, data):
                alfabe = "abcdefghijklmnopqrstuvwxyz"
                list = ['HELLO','CLOSE','REGME','GETNL']

                if data[0:5] == "HELLO":
                            response = "SALUT"
                            return response
                elif data[0:5] == "CLOSE":
                            response = "BUBYE"
                            return response
                elif data[0:5] == "REGME":
                            counter = 0
                            data_1 = data[6:].split(":")
                            ip_no = data_1[0]
                            port_no = data_1[1]
                            self.peer_ip = ip_no
                            self.peer_port = port_no
                            for k in self.fihrist.keys() :
                                if k == self.peer_port :
                                        counter = 1
                            if counter == 1 :
                                data_1 = data[6:].split(":")
                                port_no = data_1[1]
                                response = "REGOK"
                                response_1 = "REGOK"+" "+port_no
                                self.msg_1_queue.put(response_1)
                            elif counter == 0 :
                                self.control = "W"
                                d = datetime.datetime.now()
                                self.fihrist[self.peer_port] = self.peer_ip,self.cSocket,self.control_value,time.mktime(d.timetuple())
                                self.msg_1_queue.put(data)
                                return ip_no, port_no
                elif data[0:5] == "GETNL":
                            datta = data[6:]
                            nlsize = datta
                            return nlsize
                else :
                            response = "CMDER"
                            return response

            def run(self):
                while  True:
                        message = self.cSocket.recv(1024)
                        message_1 = self.parser(message)
                        print "deneme_1"
                        print (message_1)
                        print "sapanbaglari"
                        #message_2 = (message_1," ",message)
                        self.queue.put(message_1)


class Chat_Client(threading.Thread):
            def __init__(self,name,queue,msg_queue):
                threading.Thread.__init__(self)
                self.name = name
                self.queue = queue
                self.msg_queue = msg_queue
                self.peer_ip = ""
                self.peer_port = ""

            def run(self):
                print "deneme"
                while  True:
                        if self.queue.qsize > 0 :
                                    data = self.queue.get()
                                    self.peer_ip = data[0]
                                    self.peer_port = (int)(data[1])
                            
                                    try:
                                        client_Socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        client_Socket.connect((self.peer_ip,  self.peer_port))
                                    except socket.error, (value,message):
                                                if client_Socket:
                                                        response_12 = "REGOK"
                                                        response_121 = "REGOK"+" "+self.peer_port
                                                        self.msg_queue.put(response_121)

                                                print "Could not open socket: " + message

                                    response_message = "HELLO"+" "+self.peer_port
                                    self.msg_queue.put(response_message)
                                    client_read = Chat_Read_Client("ClientThread ",msg_queue,client_Socket,dict,msg_1_queue)
                                    client_read.start()





class Chat_Read_Client(threading.Thread):
            def __init__(self,name,msg_queue,sockk,fihrist,msg_1_queue):
                threading.Thread.__init__(self)
                self.name = name
                self.msg_queue = msg_queue
                self.sockk = sockk
                self.fihrist = fihrist
                self.msg_1_queue = msg_1_queue
            def parser_1(self,data_2):
                if data_2[0:5] == "HELLO":
                    response_34 = "HELLO"
                    datamania = data_2[6:]
                    for k,l,m,v in self.fihrist.values() :
                            if self.fihrist.has_key(datamania):
                                        l.send(response_34)
                elif data_2[0:5] == "CLOSE":
                     response_32 = "deneme_2"
                elif data_2[0:5] == "REGME":
                     datta = data_2[6:].split(":")
                     ip_no_1 = datta[0]
                     port_no_1 = datta[1]
                     response = "REGWA"
                     for k,l,m,v in self.fihrist.values() :
                              if self.fihrist.has_key(port_no_1):
                                        l.send(response)
                                        print "deneme_3"
                elif data_2[0:5] == "REGOK":
                             response = "REGOK"
                             port_port = data_2[6:]
                             for k,l,m,v in self.fihrist.values() :
                                if self.fihrist.has_key(port_port):
                                        l.send(response)

                elif data_2[0:5] == "REGER":
                              response = "REGER"
                              port_port = data_2[6:]
                              for k,l,m,v in self.fihrist.values() :
                                if self.fihrist.has_key(port_port):
                                            l.send(response)
                              l.close()
                              del self.fihrist[self.peer_port]


            def run(self):
                print "deneme_4"
                while True :
                        if self.msg_1_queue.qsize > 0 :
                                data_1 = self.msg_1_queue.get()
                                print data_1
                                print "deneme_5"
                                self.parser_1(data_1)
                        if self.msg_queue.qsize > 0 :
                                data_3 = self.msg_queue.get()
                                self.parser_1(data_3)
                                print "deneme_6"

                        #if self.msg_queue.qsize > 0 :
                                #data_1 = self.msg_queue.get()
                                #print data_1
                                #data_2 = data_1.split(" ")
                                #print "deneme_7"
                                #print data_1[1]
                                #for mess, sock in self.fihrist.iteritems() :
                                    #print "deneme_2"
                                    #if data_1[2] == mess :
                                        #print "deneme_8"
                                        #sock.send(str(data_1[0]))




queue = Queue.Queue()
msg_queue = Queue.Queue()
msg_1_queue = Queue.Queue()
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
    thread = Chat_Server("ChatServer",c,addr,queue,dict,msg_1_queue)
    thread.start()