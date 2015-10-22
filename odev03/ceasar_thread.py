__author__ = 'AKOLDAS'

import threading
import Queue
import sys


queue = Queue.Queue()
queueLock = threading.Lock()

exitFlag = 0

class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
    #Assign thread working with queue
        self.queue = queue

    def run(self):
        #Get from queue job

            while exitFlag == 0:
                host = self.queue.get()
                print self.getName() + ":" + host
                #signals to queue job is done
                self.queue.task_done()
                queueLock.release()

#Create number process
def function_1 (shift, n_thread, length):

    exitFlag = 0
    count = 0
    for i in range(n_thread):
        t = ThreadClass(queue)
        t.setDaemon(True)
        t.start()

    str = 'abcdefghijklmnopqrstuvwxyz'
    str_1 = ''
    i = 0
    for i in range (len(str)):
        str_1 += str[(26 -shift + i) % (len(str))]
    print(str_1)
    try :
        hostfile = open("metin.txt", "r")
    except sys.IOError as e :
        print 'could not connect to file metin.txt'


    try :
        g = open("crypted_3_3_5.txt","a")
    except sys.IOError as e :
        print 'could not connect file crypted_3_3_5.txt'
    i = 0
    while exitFlag == 0 :
        queueLock.acquire()
        if (count is not 1 ):
            c = hostfile.read(length)
            if len(c) is not length:
                exitFlag = 1
                queueLock.release()
            str_3 = c.lower()
            str_4 = ''
            i = 0
            j = 0
            for j in range (len(str_3)):
                if (str_3[j].isalpha() == False):
                                str_4 += str_3[j]
                for i in range (len(str)):
                        if (str_3[j] == str[i] ):
                            str_4 += str[(26 -shift + i)%(len(str))]

            queue.put(str_4.upper())
            g.write(str_4.upper())
            count = count + 1
        else:
            count = 0
            queueLock.release()
if __name__ == "__main__":
   function_1 (3,3,5)


queue.join()