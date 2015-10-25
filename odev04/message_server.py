__author__ = 'AKOLDAS'


import socket # Import socket module
import threading

class client(threading.Thread):
    def __init__(self,clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr

    def run(self):
        while 1 :
            print('Client sent:', self.clientSocket.recv(1024))
            #self.sock.send(b'Oi you sent something to me')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
host = "0.0.0.0" # Get local machine name
port = 12345 # Reserve a port for your service.
s.bind((host, port)) # Bind to the port

 # Now wait for client connection.
s.listen(5)
threadCounter = 0
while True:
                connection, client_addr = s.accept() # Establish connection with client.
                threadCounter += 1
                myThreadOb1 = client(connection,client_addr)
                myThreadOb1.start()



#connection.close()
#myThreadOb1.join()

