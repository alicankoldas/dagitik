__author__ = 'AKOLDAS'

# basit sunucu programi

import socket               # Import socket module
import threading


class readThread (threading.Thread):
    def __init__(self,name, clientSocket, address):
        threading.Thread.__init__(self)
        self.name = name
        self.clientSocket = clientSocket
        self.address = address
    def parser(self,data):

        data = data.strip()

        if data[0:3] == "USR":
            nickname = data[4:]
            response = "HEL" +" "+ nickname

        elif data[0:3] == "QUI":
            response = "BYE"

        elif data[0:3] == "LSQ":
            response ="LSA"

        elif data[0:3] == "TIC":
            response = "TOC"

        elif data[0:3] == "SAY":
            message = data[4:0]
            response = "SOK" +" "+ message

        elif data[0:3] == "MSG":
            response = "MOK"

        elif data[0:3] == "ERR":
            response = "hata var"
        else :
            print ("yanlis komut")

        return response

    def run(self):
       data = ""
       while  data != "bitti":
            print 'Got connection from', self.address,self.name
            data = self.clientSocket.recv(1024)
            print(data)
            data_2 = self.parser(data)
            c.send(data_2)



s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
threads = []

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   myThread_1 = readThread("Thread_1",c,addr)
   myThread_1.start()

for f in threads :
    f.join()

