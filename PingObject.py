"""
Python Project
TODO: add team membres here
TODO: documentation

Libs used:
https://docs.python.org/2/library/re.html
https://docs.python.org/2/library/subprocess.html
"""

import re
import subprocess

class PingObject:

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.addresses = set()

    def pingHosts(self):
        try:
            # Ping hosts with the broadcast address
            process = subprocess.Popen("ping -c 2 " + str(self.ip_address), stdout = subprocess.PIPE, shell = True)
            (out, err) = process.communicate()
            # Check the output from the ping
            for line in out.splitlines():
                match = re.search(r'^\d+\s+bytes\s+from\s+(?P<IP>.*):\s+icmp_seq=\d+\s+ttl=\d+\s+time=.*$', line, re.MULTILINE)
                if match:
                    # If output matches, add address into a set
                    self.addresses.add(match.group('IP'))
        except OSError:
            # Return None if an error has occured
            return None
        # Return the set
        return self.addresses
