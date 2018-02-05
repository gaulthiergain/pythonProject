"""
Python Project
TODO: add team membres here

Libs used:
https://docs.python.org/2/library/re.html

"""

import re

filenameRange = 'range.txt'
filenamePwd = 'password.txt'

#Begin to read range file
try:
    file = open(filenameRange, 'r')
    while True:
        ip_add = ''.join(file.readline().splitlines())
        if (ip_add == ''):
            break
        print '[' + ip_add + ']'
        #test
except IOError:
    print 'The file' + filenameRange + ' couldn\'t be found'
    exit()

