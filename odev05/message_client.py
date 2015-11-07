__author__ = 'AKOLDAS'
# basit bir client

__author__ = 'AKOLDAS'

import socket               # Import socket module
import threading

class writeThread_1(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name

    def run (self):
        string_1 = ''
        while string_1 != 'bitti':
            string_1 = raw_input("Enter your input: ")
            print('input value %s in thread %s' % (string_1, self.name))
            s.send(string_1)
            print s.recv(1024)



s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.connect((host, port))

myThreadOb1 = writeThread_1('Thread 1')
myThreadOb1.start()
myThreadOb1.join()
s.close