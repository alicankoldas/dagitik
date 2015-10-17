__author__ = 'AKOLDAS'

import numpy as np
import string as st
import sys


def function_1(shift, thread_number, length):

    try :
        f = open("metin.txt", "r")
        a = f.read()
    except sys.IOError as e :
        print 'could not connect to file metin.txt'

    f.close()

    str = 'abcdefghijklmnopqrstuvwxyz'
    str_1 = ''
    i = 0
    for i in range (len(str)):
        str_1 += str[(i+shift)%(len(str))]


    print(str_1)
    print(len(str_1))

    str_3 = a
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

    print(len(str_3))
    print(str_4)
    print(len(bosluk))

    try :
        g = open("crypted_3_3_5.txt","a")
        g.write(str_4)
        g.close()
    except sys.IOError as e :
        print 'could not connect file crypted_3_3_5.txt'



function_1(3,3, 5)

