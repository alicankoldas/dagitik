__author__ = 'AKOLDAS'

import socket               # Import socket module
import threading
from multiprocessing import Queue
import random
from multiprocessing import Lock
import time


dict = {}
lock = Lock()
logFile = "log_file.txt"

class LoggerThread (threading.Thread):
    def __init__(self,name,logQueue,logFileName):
        threading.Thread.__init__(self)
        self.name = name
        self.logQueue = logQueue
        self.logFileName = open(logFile,"a")


    def log(self,message):
            t = time.ctime()
            self.logFileName.write(t + message+"\n")
            self.logFileName.flush()

    def run (self):
        self.log("Starting"+" "+self.name)
        while True :
            if self.logQueue.qsize() > 0 :
                message_123 = self.logQueue.get()
                self.log(message_123)
        self.log("Exiting"+" "+self.name)
        self.logFileName.close()

class readThread (threading.Thread):
    def __init__(self,clientSocket, address,threadQueue,fihrist,logQueue):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.address = address
        self.threadQueue = threadQueue
        self.fihrist = fihrist
        self.logQueue = logQueue

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
                    self.fihrist[self.nickname] = self.clientSocket
                    self.logQueue.put(self.nickname+" "+"has join\n")

                else :
                            response = "REJ"+" "+self.nickname
                print self.fihrist

            elif data[0:3] == "QUI":
                for k,l in self.fihrist.iteritems() :
                    if l == self.clientSocket :
                        response = "BYE" + str(k)
                try:
                    del self.fihrist[k]
                    print self.fihrist
                    self.logQueue.put(self.k+" "+"has left"+"\n")
                except KeyError:
                    pass


            elif data[0:3] == "LSQ":
                response ="LSA" + str(self.fihrist.keys())

            elif data[0:3] == "TIC":
                response = "TOC"


            elif data[0:3] == "SAY":
                message = data[4:]
                print message
                is_there_user = 0
                response = "SOK"
                to_nick = ""
                for nick , sock in self.fihrist.iteritems() :
                        if sock == self.clientSocket :
                            from_nick = nick
                            is_there_user = 1

                            self.threadQueue.put((to_nick,from_nick,message))


                if is_there_user == 0 :
                    response = "ERL"

            elif data[0:3] == "MSG":
                is_there_user = 0
                data_1 = data[3:]
                data_1 = data_1.strip()
                word = data_1.split(':')
                to_nick = word[0]
                print to_nick
                message = word[1]
                print message
                for nick , sock in self.fihrist.iteritems() :
                        if sock == self.clientSocket :
                            print "evveettttt"
                            from_nick = nick
                            print from_nick
                            is_there_user = 1

                            self.threadQueue.put((to_nick,from_nick,message))

                if is_there_user == 1 :
                    response = "MOK"
                if is_there_user == 0 :
                    response = "MNO"+" "+from_nick

            else :
                response = "yanlis komut"

            return response



    def run(self):

       data = ""
       cur_thread = threading.currentThread()
       print "Starting"+ cur_thread.getName()
       self.logQueue.put("Starting Read"+cur_thread.getName()+"\n")
       while  data != "bitti":
            #print 'Got connection from', self.address,cur_thread.getName()
            data = self.clientSocket.recv(1024)
            print(data)

            data_1 = self.parser(data)
            #lock.acquire()
            self.threadQueue.put(data_1)
            #lock.release()
       self.logQueue.put("Exiting Read"+cur_thread.getName()+"\n")
       print "Exiting" + cur_thread.getName()

class writeThread (threading.Thread):
    def __init__(self,cSocket, address,threadQueue,fihrist,logQueue):
        threading.Thread.__init__(self)
        self.cSocket = cSocket
        self.address = address
        self.threadQueue = threadQueue
        self.fihrist = fihrist
        self.logQueue = logQueue

    def run(self):

       cur_thread = threading.currentThread()
       #l.acquire()
       print "Starting"+ cur_thread.getName()
       #l.release()
       self.logQueue.put("Starting Write"+cur_thread.getName())
       while  True :

         if  self.threadQueue.qsize() > 0:
                sayac = 0
                tuple_1 = ['LSA','BYE','TIC','HEL','REJ','SOK','MOK','MNO','ERR','ERL']
                #lock.acquire()
                queue_message = self.threadQueue.get()
                #lock.release()
                print queue_message

                data_1 = queue_message[0:3]
                for i in tuple_1 :
                    if data_1 == i :
                        sayac = 1
                if sayac == 1 :
                    self.cSocket.send(queue_message)

                if sayac == 0 :
                    print "bulundunuz araniyorsunuz"
                    queue_message_1 = repr(queue_message)
                    print "naber"
                    data_2 = queue_message_1.split(',')
                    print data_2[0]
                    if data_2[0] == "(''":
                        print "ah sen ne guzel guluyorsun"
                        print self.fihrist
                        for nick, sock in self.fihrist.iteritems() :
                            sock.send(data_2[2])
                    else :
                        print "neredesin nerde???"
                        print data_2[0]
                        data_2[0] = str = data_2[0].replace("'","").replace("(","").replace(")","")
                        for nick, sock in self.fihrist.iteritems() :
                            print nick
                            if data_2[0] == nick :
                              sock.send(data_2[2])




       print "Exiting" + cur_thread.getName()
       self.logQueue.put("Exiting Write"+cur_thread.getName())


s = socket.socket()         # Create a socket object
host = "127.0.0.1" # Get local machine name
port = 9996                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
threads_1 = []
threads_2 = []
threads_3 = []
logQ = Queue()
name = "LoggerThread"
               # Now wait for client connection.
myThread_3 = LoggerThread(name,logQ,logFile)
#myThread_3.setDaemon()
myThread_3.start()
s.listen(5)


while True:
   logQ.put("Waiting for connection\n")
   c, addr = s.accept()     # Establish connection with client.
   logQ.put("Got connection from"+str(c)+" "+str(addr)+"\n")
   threadQ = Queue()

   myThread_1 = readThread(c,addr,threadQ,dict,logQ)
   myThread_2 = writeThread(c,addr,threadQ,dict,logQ)

   myThread_1.setDaemon(True)
   myThread_1.start()
   myThread_2.setDaemon(True)
   myThread_2.start()

   threads_1.append(myThread_1)
   threads_2.append(myThread_2)
   threads_3.append(myThread_3)

logQ.put("Closing socket "+str(c)+" "+str(addr)+"\n")

for f in threads_1 :
    f.join()

for g in threads_2 :
    g.join()

for h in threads_3 :
    h.join()