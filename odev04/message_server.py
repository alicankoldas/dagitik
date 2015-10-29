__author__ = 'AKOLDAS'


import socket
import threading
import time
import datetime

import random

class client(threading.Thread):
    def __init__(self,clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr

    def run(self):
        k = 0
        rakam_1 = 4
        print "Connection established:"
        data = "deneme"

        while len(data) :
            data = self.clientSocket.recv(1024)
            adres = 'Peki',client_addr
            rakam_2 =  random.randint(1, 10)
            print(rakam_2) # rakam dort oldugu zaman sunucu istemciye bildirimde bulunur
            if (rakam_2 == rakam_1):
                now = datetime.datetime.now()
                string_3 = datetime.time(now.hour, now.minute, now.second)
                string_4 = "Merhaba saat su an",string_3
                self.clientSocket.send(str(string_4))

            if data != "bitti":
                self.clientSocket.send(str(adres))
            else :
                self.clientSocket.send(str(data))
            print('Client sent:', data)

        print "Client disconnected..."

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
host = "0.0.0.0" # Get local machine name
port = 12345 # Reserve a port for your service.
s.bind((host, port)) # Bind to the port
threads = []


while True:
               s.listen(5)
               connection, client_addr = s.accept()
               myThreadOb1 = client(connection,client_addr)
               myThreadOb1.start()
               threads.append(myThreadOb1)



for t in threads :
    t.join()

