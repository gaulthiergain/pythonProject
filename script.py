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

filenamePwd = 'password.txt'

"""
Method allowing to read a range of ip addresses
"""
def GetAddressHosts(filenameRange):
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
            return pingObject.pingHosts()

    except ValueError:
        print 'Invalid IP address format'
        sys.exit(0)
    except IOError:
        print 'The file' + filenameRange + ' couldn\'t be found'
        sys.exit(0)

# Read range first
filenameRange = 'range.txt'
up_hosts = GetAddressHosts(filenameRange)
if up_hosts is None:
    print 'Couldn\'t ping devices'
    sys.exit(0)
else:
    #TODO remove (just for display)
    for host in up_hosts:
        print host

#Read password file
passwords = set()
try:
    file = open(filenamePwd, 'r')
    while True:
        password = ''.join(file.readline().splitlines())
        if (password == ''):
            break

        passwords.add(password)
except IOError:
    print 'The file' + filenamePwd + ' couldn\'t be found'
    sys.exit(0)

#TODO remove (just for display)
for passw in passwords:
    print passw
