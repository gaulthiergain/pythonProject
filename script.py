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

"""
Method allowing to read a range of ip addresses from a file
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

"""
Method allowing to read passwords from a file
"""
def ReadPasswords(filenamePwd):
    passwords = set()
    try:
        file = open(filenamePwd, 'r')
        while True:
            password = ''.join(file.readline().splitlines())
            if (password == ''):
                break

            # Add current password to a set of passwords
            passwords.add(password)
        return passwords
    except IOError:
        print 'The file' + filenamePwd + ' couldn\'t be found'
        sys.exit(0)

# 1. Read range first
filename_range = 'range.txt'
up_hosts = GetAddressHosts(filename_range)
if up_hosts is None:
    print 'Couldn\'t ping devices'
    sys.exit(0)
else:
    #TODO remove (just for display)
    for host in up_hosts:
        print host

# 2. Read passwords file
filename_pwd = 'password.txt'
passwords = ReadPasswords(filename_pwd)
if passwords is None:
    print 'Empty passwords list'
    sys.exit(0)
else:
    #TODO remove (just for display)
    for password in passwords:
        print password
