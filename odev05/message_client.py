__author__ = 'AKOLDAS'

import socket               # Import socket module
import threading
from multiprocessing import Queue
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys





class ReadThread_Client (threading.Thread):
    def __init__(self,name,cSocket,threadQueue_1,app):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.nickname = ""
        self.threadQueue_1 = threadQueue_1
        self.app = app

    def incoming_parser(self,data):
        response = ""
        if data[0:3] == 'HEL':
            response = data
            self.app.cprint(response)
        elif data [0:3] == 'REJ' :
            response = data
            self.app.cprint(response)
        elif data[0:3] == 'SOK':
            response = data
            self.app.cprint(response)
        elif data[0:3] == 'TOC':
            response = data
            self.app.cprint(response)
        elif data[0:3] == 'LSA':
            response == data
            self.app.cprint(response)
        elif data[0:3] == 'ERR':
            response = data
            self.app.cprint(response)
        elif data[0:3] == 'ERL':
            response = data
            self.app.cprint(response)
        elif data[0:3] == 'MOK':
            response = data
            self.app.cprint(response)
        elif data[0:3] == 'MNO' :
            response = data
            self.app.cprint(response)
        elif data[0:3] == 'BYE' :
            response = data
            self.app.cprint(response)
        else :
            #print data
            data = data.replace("'","").replace("(","").replace(")","").replace(",","")
            #print data
            response = data
            self.app.cprint(response)



    def run(self) :
         while True :
            data = self.cSocket.recv(1024)
            #print(data)
            #data_1234 = self.incoming_parser(data)
            #print data_1234
            self.incoming_parser(data)
            #self.threadQueue_1.put(data_1234)

class WriteThread_Client (threading.Thread) :
    def __init__(self,name,csoc,threadQueue_1):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.threadQueue_1 = threadQueue_1

    def run(self):
            while True :

                ####if self.threadQueue_1.qsize() == 0 :
                ####    string_1 = raw_input("Enter your input: ")

                if self.threadQueue_1.qsize() > 0 :
                    print "*******"
                    kuyruk_mesaji = self.threadQueue_1.get()
                    print kuyruk_mesaji
                    print "*******"

                    self.csoc.send(str(kuyruk_mesaji))
                    #print('input value %s in thread %s' % (string_1, self.name))

                #if self.threadQueue_1.qsize() > 0:


class ClientDialog(QDialog) :

    def __init__(self, threadQueue):
        self.threadQueue = threadQueue

        self.qt_app = QApplication(sys.argv)

        QDialog.__init__(self,None)

        self.setWindowTitle('IRC Client')
        self.setMinimumSize(500,200)

        self.vbox = QVBoxLayout()

        self.sender = QLineEdit("", self)

        self.channel = QTextBrowser()

        self.send_button = QPushButton('&Send')

        self.send_button.clicked.connect(self.outgoing_parser)

        self.vbox.addWidget(self.channel)
        self.vbox.addWidget(self.sender)
        self.vbox.addWidget(self.send_button)

        self.setLayout(self.vbox)

    def cprint (self,data):

        self.channel.append(data)

    def outgoing_parser(self):
        data = self.sender.text()
        print data
        self.cprint(data)
        command =""
        nickname_1 = ""
        nickname_2 = ""
        message_1 = ""
        if len(data) == 0:
            return
        if data[0] == "/":
            data_bestvan = data.split(" ")
            print data_bestvan
            if data_bestvan[1] == "nick":
                nickname_1 = data_bestvan[2]
                self.threadQueue.put("USR"+" "+nickname_1)
            elif data_bestvan[1] == "list":
                self.threadQueue.put("LSQ")
            elif data_bestvan[1] == "quit":
                self.threadQueue.put("QUI")
            elif data_bestvan[1] == "msg":
                nickname_2 = data_bestvan[2]
                message_1 = data_bestvan[3]
                self.threadQueue.put("MSG"+" "+nickname_2+" "+message_1)
            else :
                self.cprint("Local: Command Error.")
        else :
            self.threadQueue.put("SAY"+" "+data)
        self.sender.clear()

    def run(self):

        '''Run the app and show the main from.'''
        self.show()
        self.qt_app.exec_()



s = socket.socket()         # Create a socket object
host = "127.0.0.1" # Get local machine name
port = 9996               # Reserve a port for your service.
s.connect((host, port))
sendQueue = Queue()

app = ClientDialog(sendQueue)

myThreadOb1 = ReadThread_Client("ReadThread",s,sendQueue,app)
myThreadOb1.start()
myThreadOb2 = WriteThread_Client("WriteThread",s,sendQueue)
myThreadOb2.start()

app.run()

myThreadOb1.join()
myThreadOb2.join()
s.close()



