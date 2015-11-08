__author__ = 'AKOLDAS'

import socket               # Import socket module
import threading
from multiprocessing import Queue
import random
from multiprocessing import Lock



l = Lock()
class readThread (threading.Thread):
    def __init__(self,clientSocket, address,threadQueue,fihrist):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.address = address
        self.threadQueue = threadQueue
        self.fihrist = fihrist

    def parser(self,data):
            response = ""
            alfabe = "abcdefghijklmnopqrstuvwxyz"
            list = ['USR','QUI','TIC','SAY','MSG','LSQ']
            self.nickname = data[4:]
            y = 0
            h = 0
            c = 0
            for i in self.nickname:
                if i == " ":
                    h = 1

            if h == 1 :
                response = "REJ" + self.nickname
            for i in alfabe:
                for j in self.nickname :
                    if i != j:
                        y = 1
            if y==1:
                response = "REJ" + self.nickname
            data = data.strip()

            if not self.nickname and not data[0:3] == "USR":
                response = "ERL"
            for i in list :
                if c != data[0:3]:
                   c = c + 1
            if c == 6 :
                response = "ERR"

            if data[0:3] == "USR":
                p = 0
                for k in self.fihrist.keys() :
                    if self.nickname == k :
                       p = p + 1
                if p ==  0:
                    response = "HEL" +" "+ self.nickname
                    self.fihrist[self.nickname] = self.threadQueue
                else :
                            response = "REJ"+" "+self.nickname
                print self.fihrist

            elif data[0:3] == "QUI":
                for k,l in self.fihrist.iteritems() :
                    if l == self.threadQueue :
                        response = "BYE" + str(k)
                try:
                    del self.fihrist[k]
                    print self.fihrist
                except KeyError:
                    pass


            elif data[0:3] == "LSQ":
                response ="LSA" + str(self.fihrist.keys())

            elif data[0:3] == "TIC":
                response = "TOC"


            elif data[0:3] == "SAY":
                message = data[4:0]
                response = "SOK" +" "+ message

            elif data[0:3] == "MSG":
                response = "MOK"

            else :
                response = "yanlis komut"

            return response



    def run(self):

       data = ""
       cur_thread = threading.currentThread()
       print "Starting"+ cur_thread.getName()
       while  data != "bitti":
            l.acquire()
            print 'Got connection from', self.address,cur_thread.getName()
            l.release()
            data = self.clientSocket.recv(1024)
            print(data)
            data_1 = self.parser(data)

            self.threadQueue.put(data_1)

       print "Exiting" + cur_thread.getName()

class writeThread (threading.Thread):
    def __init__(self,cSocket, address,threadQueue):
        threading.Thread.__init__(self)
        #self.name = name
        self.cSocket = cSocket
        self.address = address
        self.threadQueue = threadQueue

    def run(self):

       cur_thread = threading.currentThread()
       l.acquire()
       print "Starting"+ cur_thread.getName()
       l.release()
       while  True :

         if  self.threadQueue.qsize() > 0:
                queue_message = self.threadQueue.get()
                self.cSocket.send(queue_message)

       print "Exiting" + cur_thread.getName()


s = socket.socket()         # Create a socket object
host = "127.0.0.1" # Get local machine name
port = 9999                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
threads_1 = []
threads_2 = []
threadQ = Queue()
dict = {}
s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   myThread_1 = readThread(c,addr,threadQ,dict)
   myThread_2 = writeThread(c,addr,threadQ)
   myThread_1.start()
   myThread_2.start()
   threads_1.append(myThread_1)
   threads_2.append(myThread_2)

for f in threads_1 :
    f.join()

for g in threads_2 :
    g.join()