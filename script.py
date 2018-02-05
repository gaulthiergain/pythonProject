"""
Python Project
TODO: add team membres here

Libs used:
https://docs.python.org/2/library/re.html
https://docs.python.org/3/library/ipaddress.html
"""

import re
import ipaddress
import sys

from PingObject import PingObject

filenameRange = 'range.txt'
filenamePwd = 'password.txt'

#Begin to read range file
try:
    file = open(filenameRange, 'r')
    while True:
        ip_add = ''.join(file.readline().splitlines())
        if (ip_add == ''):
            break

        # Use ipaddress module to check the validity of ip address
        ip_network = ipaddress.ip_network(unicode(ip_add, "UTF-8"), strict = False)
        broadcast_address = ip_network.broadcast_address

        # Ping all devices from the broadcast address using subprocess
        pingObject = PingObject(broadcast_address)
        upHosts = pingObject.pingHosts()

        if upHosts is None:
            print 'Couldn\'t ping devices'
            sys.exit(0)
        else:
            #TODO remove (just for display)
            for host in upHosts:
                print host

except ValueError:
    print 'Invalid IP address format'
    sys.exit(0)
except IOError:
    print 'The file' + filenameRange + ' couldn\'t be found'
    sys.exit(0)
