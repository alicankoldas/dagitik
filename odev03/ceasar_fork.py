__author__ = 'AKOLDAS'

import sys
import time

from multiprocessing import Process, Queue, Lock, current_process


exitFlag = 0
l = Lock()

def worker(done_queue,work_queue):

  try:
        for string_1 in iter(work_queue.get, 'STOP'):
            done_queue.put("%s - %s" % (current_process().name, string_1))
            print current_process().name + ":"+ string_1
  except sys.Exception, e:
        done_queue.put("%s failed on %s" % (current_process().name, string_1))
  return True


def print_string(shift, process_number, length):

    done_queue = Queue()
    work_queue = Queue()

    processes = []

    exitFlag = 0
    count = 0

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
        l.acquire()
        if (count is not 1 ):

            c = hostfile.read(length)

            if len(c) is not length:
                exitFlag = 1

            str_3 = c.lower()
            str_4 = ''
            i = 0
            j = 0
            for j in range (len(str_3)):
                if (str_3[j].isalpha() == False):
                                str_4 += str_3[j]
                for i in range (len(str)):
                        if (str_3[j] == str[i] ):
                            str_4 += str[(i+shift)%(len(str))]
            g.write(str_4.upper())

            work_queue.put(str_4.upper())
            #print(str_4.upper())
            count = count + 1
            l.release()
        else:
            count = 0
            l.release()

    for w in xrange(process_number):
        p = Process(target=worker,args = (done_queue,work_queue))
        p.start()
        processes.append(p)
        work_queue.put('STOP')

    for p in processes:
        p.join()

    done_queue.put('STOP')


if __name__ == "__main__":
      print_string(3,3,5)

