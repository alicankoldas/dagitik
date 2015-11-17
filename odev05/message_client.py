__author__ = 'AKOLDAS'

import socket               # Import socket module
import threading
from multiprocessing import Queue
from PyQt4 import QtCore
from PyQt4.QtGui import *
import sys


id = QtCore.QMetaType.type('MyClass')


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
            nickname_2 = ""
            if data[0:3] == 'HEL':
                    response = data
                    print "Server response : "+response # burada console ekranina dogrudan sunucu tarafindan gelen mesaji bastiriyorum gorun diye orijinal mesaji
                    nickname_2 = data[4:]
                    self.app.cprint("-Server- Registered as <"+nickname_2+">")
            if data [0:3] == 'REJ' :
                    response = data
                    print "Server response : "+response
                    nickname_2 = data[4:0]
                    self.app.cprint("-Server-"+nickname_2+"not registered")
            if data[0:3] == 'SOK':
                    response = data
                    print "Server response : "+response
                    self.app.cprint("-Server- "+response)
            if data[0:3] == 'TOC':
                    response = data
                    print "Server response : "+response
                    self.app.cprint("-Server- "+response)
            if data[0:3] == 'LSA':
                    response == data
                    print "Server response : "+response

                    self.app.cprint("-Server- "+response)
            if data[0:3] == 'ERR':
                    response = data
                    print "Server response : "+response
                    self.app.cprint("-Server- "+response)
            if data[0:3] == 'ERL':
                    response = data
                    print "Server response : "+response
                    self.app.cprint("-Server- "+response)
            if data[0:3] == 'MOK':
                    response = data
                    print "Server response : "+response
                    self.app.cprint("-Server- "+response)
            if data[0:3] == 'MNO' :
                    response = data
                    print "Server response : "+response
                    self.app.cprint("-Server- "+response)
            if data[0:3] == 'BYE' :
                    response = data
                    print "Server response : "+response
                    self.app.cprint("-Server- "+response)
            else :
                    data = data.replace("'","").replace("(","").replace(")","").replace(",","")
                    response = data
                    print "Server response : "+response
                    self.app.cprint("-Server- "+response)



    def run(self) :
            while True :
                    data = self.cSocket.recv(1024)
                    self.incoming_parser(data)


class WriteThread_Client (threading.Thread) :
    def __init__(self,name,csoc,threadQueue_1):
        threading.Thread.__init__(self)
        self.name = name
        self.csoc = csoc
        self.threadQueue_1 = threadQueue_1

    def run(self):
            while True :

                if self.threadQueue_1.qsize() > 0 :
                    kuyruk_mesaji = self.threadQueue_1.get()
                    print "istemci tarifindan gonderilen mesaj : "+kuyruk_mesaji

                    self.csoc.send(str(kuyruk_mesaji))



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
        print "Kullanicinin arayuzden girdigi mesaj : "+data
        self.cprint("Local:- "+data)
        command =""
        nickname_1 = ""
        nickname_2 = ""
        message_1 = ""
        if len(data) == 0:
            return
        if data[0] == "/":
                incoming_client_interface_data = data.split(" ")  # istemci arayuzu tarfindan girilen data
                #print "Kullanicinin arayuzden girdigi mesaj : "+str(incoming_client_interface_data) # istemci console ekranina bastir
                if incoming_client_interface_data[1] == "nick":
                        nickname_1 = incoming_client_interface_data[2]
                        self.threadQueue.put("USR"+" "+nickname_1)
                elif incoming_client_interface_data[1] == "list":
                        self.threadQueue.put("LSQ")
                elif incoming_client_interface_data[1] == "quit":
                        self.threadQueue.put("QUI")
                elif incoming_client_interface_data[1] == "msg":
                        nickname_2 = incoming_client_interface_data[2]
                        message_1 = incoming_client_interface_data[3]
                        self.threadQueue.put("MSG"+" "+nickname_2+":"+message_1)
                elif incoming_client_interface_data[1] == "connexion": # kendim ekledim baglanti kontrol durumu icin
                        self.threadQueue.put("TIC")
                else :
                        self.cprint("Local: Command Error.")
        else :
                self.threadQueue.put("SAY"+" "+data)
        self.sender.clear()

    def run(self):

        '''Run the app and show the main from.'''
        self.show()
        self.qt_app.exec_()



s = socket.socket()         # soket objesini yarat
host = "127.0.0.1" # locale machine hostu al
port = 9996               #  port numarasi
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



