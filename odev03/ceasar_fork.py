__author__ = 'AKOLDAS'

import sys

from multiprocessing import Process, Queue, Lock, current_process


exitFlag = 0

def worker(work_queue, done_queue):
            print_string(3,3,5)
            done_queue.put("%s" % (current_process().name))
            return True

def print_string(shift, process_number, length):

        exitFlag = 0
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
        count = 0
        while exitFlag == 0 :
            if ( count is not 1 ):
                c = hostfile.read(length)
                if len(c) is not length:
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
                g.write(str_4)
                count = count + 1
            else:
                count = 0


if __name__ == "__main__":

        work_queue = Queue()
        done_queue = Queue()
        processes = []
        process_number = 3

        for w in xrange(process_number):
            p = Process(target=worker, args=(work_queue, done_queue))
            p.start()
            processes.append(p)
            work_queue.put('STOP')

        for p in processes:
            p.join()

        done_queue.put('STOP')