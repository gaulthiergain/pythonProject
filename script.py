"""
Python Project (Cisco Incubator 2018)

Constributors:
- Boriychuk Dima
- Gain Gaulthier

Libs used:
- https://docs.python.org/2/library/re.html
- https://docs.python.org/3/library/ipaddress.html
- https://docs.python.org/2/library/sys.html
- https://networkx.github.io
- https://matplotlib.org
"""

import re
import ipaddress
import sys
import networkx as nx
import matplotlib.pyplot as plt

from GetRouterID import GetRouterID
from PingObject import PingObject
from HTMLoutput import HTML

"""
Method allowing to read ip addresses from a file
"""
def readRange(filenameRange):
    up_hosts = set()
    try:
        with open(filenameRange) as file:
            content = file.readlines()

            # Save ranges into a list
            ranges = [x.strip() for x in content]

            # Iterate over each range
            for ip_add in ranges:
                # Use ipaddress module to check the validity of ip range
                ip_network = ipaddress.ip_network(unicode(ip_add, "UTF-8"), strict = False)
                # Add all discovered devices into a set
                up_hosts.update(getUpHosts(ip_network))

            return up_hosts

    except ValueError:
        print 'Invalid IP address format'
        sys.exit(0)
    except IOError:
        print 'The file' + filenameRange + ' couldn\'t be found'
        sys.exit(0)

"""
Method allowing to compute broadcast_address and to ping hosts that are up
"""
def getUpHosts(ip_network):
    # Get broadcast_address from ip network
    broadcast_address = ip_network.broadcast_address

    # Ping all devices from the broadcast address using subprocess
    pingObject = PingObject(broadcast_address)
    return pingObject.pingHosts()

"""
Method allowing to read passwords from a file
"""
def readPasswords(filenamePwd):
    try:
        with open(filename_pwd) as file:
            content = file.readlines()

        # Return all the passwords as a list
        return [x.strip() for x in content]
    except IOError:
        print 'The file' + filenamePwd + ' couldn\'t be found'
        sys.exit(0)

# 1. Read range first
print 'Reading rante.txt file and detecting active IP'
filename_range = 'range.txt'
up_hosts = readRange(filename_range)
if up_hosts is None:
    print 'Couldn\'t ping devices'
    sys.exit(0)

# 2. Read passwords file
print 'Reading password.txt file'
filename_pwd = 'password.txt'
passwords = readPasswords(filename_pwd)
if passwords is None:
    print 'Empty passwords list'
    sys.exit(0)

# 3. Connect and collect info
print 'Connecting to the routers and collecting information'
GetRouterID = GetRouterID (up_hosts, passwords)
dev = GetRouterID.GetID()
 
# 4. Get info about End Of Life
print 'Requesting to the API for End of Life dates'
EoL = GetRouterID.getEoL()

# 5. Output results into .html file and show it
html = HTML (dev, EoL)
html.createHTML()

# 6. Build topology
print 'Building the topology'
G = nx.Graph()

for key in GetRouterID.neighbors:
    G.add_node(str(key))
    for values in GetRouterID.neighbors[str(key)]:
        G.add_edge(key, values)

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
