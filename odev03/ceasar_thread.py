__author__ = 'AKOLDAS'



import threading
import Queue
import sys

#Number of threads
n_thread = 3
#Create queue
queue = Queue.Queue()
queueLock = threading.Lock()

exitFlag = 0

class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
    #Assign thread working with queue
        self.queue = queue

    def run(self):
        while not exitFlag :
        #Get from queue job
            queueLock.acquire()
            host = self.queue.get()
            print self.getName() + ":" + host
        #signals to queue job is done
            self.queue.task_done()
            queueLock.release()

#Create number process
for i in range(n_thread):
    t = ThreadClass(queue)
    t.setDaemon(True)
    t.start()

count = 0
shift = 3
n = 5
str = 'abcdefghijklmnopqrstuvwxyz'
str_1 = ''
i = 0
for i in range (len(str)):
    str_1 += str[(i+shift)%(len(str))]

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
    if ( count is not 1 ):
        c = hostfile.read(n)
        if len(c) is not n:
            exitFlag = 1
        str_3 = c
        str_4 = ''
        i = 0
        j = 0
        bosluk = " "
        for j in range (len(str_3)):
            for i in range (len(str)):
                if (str_3[j] == str[i]):
                    str_4 += str[(i+shift)%(len(str))]
                elif str_3[j] == bosluk :
                    str_4 += bosluk
        queue.put(str_4)
        g.write(str_4)
        count = count + 1
    else:
        count = 0

exitFlag = 1


queue.join()



