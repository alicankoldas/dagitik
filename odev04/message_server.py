__author__ = 'AKOLDAS'


import socket # Import socket module
import threading
import time

class client(threading.Thread):
    def __init__(self,clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr

    def run(self):
        print "Connection established:"
        data = "deneme"
        while len(data) :
            data = self.clientSocket.recv(1024)
            if data:
                adres = 'Peki',client_addr
                self.clientSocket.send(str(adres))
            print('Client sent:', data)
            #self.sock.send(b'Oi you sent something to me')
        print "Client disconnected..."

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
host = "0.0.0.0" # Get local machine name
port = 12345 # Reserve a port for your service.
s.bind((host, port)) # Bind to the port
threads = []
 # Now wait for client connection.

threadCounter = 0
while True:
               s.listen(5)
               connection, client_addr = s.accept() # Establish connection with client.
               threadCounter += 1
               myThreadOb1 = client(connection,client_addr)
               myThreadOb1.start()
               threads.append(myThreadOb1)



#s.close()
#connection.close()

for t in threads :
    t.join()

