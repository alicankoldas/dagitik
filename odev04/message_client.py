__author__ = 'AKOLDAS'


import random
import threading
from random import randint
import socket
import sys
import time

class writeThread(threading.Thread):
    def __init__(self, name):
        ''' Constructor. '''
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
         string_1 = ''
         while string_1 != 'bitti':
             string_1 = raw_input("Enter your input: ")
             print('input value %s in thread %s' % (string_1, self.name))
              # Sleep for random time between 1 ~ 3 second
             sock.send(string_1)
             data_1 = sock.recv(1024)
             secondsToSleep = randint(1, 5)
             print('%s sleeping fo %d seconds...' % (self.name, secondsToSleep))
             print data_1
             time.sleep(secondsToSleep)


if __name__ == "__main__":
   # Declare objects of MyThread class
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 12345
    sock.connect((host,port))

    myThreadOb1 = writeThread('Thread 1')

   # Start running the threads!
    myThreadOb1.start()

   # Wait for the threads to finish...
    myThreadOb1.join()

    print('Main Terminating...')

    sock.close()





