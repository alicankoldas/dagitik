__author__ = 'AKOLDAS'

import socket               # Import socket module
import threading
from multiprocessing import Queue
import time





class ReadThread_Client (threading.Thread):
    def __init__(self,name,cSocket,threadQueue_1):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.nickname = ""
        self.threadQueue_1 = threadQueue_1

    def incoming_parser(self,data):
        response = ""
        if data[0:3] == 'HEL':
            response = data
        elif data [0:3] == 'REJ' :
            response = data
        elif data[0:3] == 'SOK':
            response = data
        elif data[0:3] == 'TOC':
            response = data
        elif data[0:3] == 'LSA':
            response == data
        elif data[0:3] == 'ERR':
            response = data
        elif data[0:3] == 'ERL':
            response = data
        elif data[0:3] == 'MOK':
            response = data
        elif data[0:3] == 'MNO' :
            response = data
        elif data[0:3] == 'BYE' :
            response = data
        else :
            #print data
            data = data.replace("'","").replace("(","").replace(")","").replace(",","")
            #print data
            response = data
        return response

    def run(self) :
         while True :
            data = self.cSocket.recv(1024)
            #print(data)
            data_1234 = self.incoming_parser(data)
            #print data_1234
            self.threadQueue_1.put(data_1234)

class WriteThread_Client (threading.Thread) :
    def __init__(self,name,csoc,threadQueue_1):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.threadQueue_1 = threadQueue_1

    def run(self):
            while True :

                if self.threadQueue_1.qsize() == 0 :
                    string_1 = raw_input("Enter your input: ")

                if self.threadQueue_1.qsize() > 0 :
                    print "*******"
                    kuyruk_mesaji = self.threadQueue_1.get()
                    print kuyruk_mesaji
                    print "*******"

                self.csoc.send(string_1)
                    #print('input value %s in thread %s' % (string_1, self.name))

                #if self.threadQueue_1.qsize() > 0:







s = socket.socket()         # Create a socket object
host = "127.0.0.1" # Get local machine name
port = 9996               # Reserve a port for your service.
s.connect((host, port))
sendQueue = Queue()
myThreadOb1 = ReadThread_Client("ReadThread",s,sendQueue)
myThreadOb1.start()
myThreadOb2 = WriteThread_Client("WriteThread",s,sendQueue)
myThreadOb2.start()
myThreadOb1.join()
myThreadOb2.join()
s.close()



