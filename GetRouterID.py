#TODO revise collected ifno
#TODO check why only one result is displeyed

"""
#Libs used: re, netmiko

"""
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException
import re
import threading

class GetRouterID:
    # Need list of available hosts and list of passwords
    def __init__ (self, hosts, passwords):
        self.hosts = hosts
        self.passwords = passwords
        self.devices = []
        self.neighbors = {}

    def find_password(self, host, ID):

        for password in self.passwords:
            try:
                session = ConnectHandler(device_type = 'cisco_ios',
                                         ip = host,
                                         username = 'admin',
                                         password = password,
                                         secret = password)
                if session.is_alive():
                    ID['Password'] = password
                    return session
                    break
            except NetMikoAuthenticationException:
                continue

    def GetID(self):
         # added threads
        threads = []
        for host in self.hosts:
            th = threading.Thread (target = self.connect, args = (host,))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()
        return self.devices

    def connect(self, host):
        #ID structure:
        #{'Host': string, 'Password': string, 'IOS version': string, 'Hardware version': string,
        #'Modules': dictionary, 'Interfaces': dictionary}
        #
        #'Modules': dictionary {'Slot(n)': string}
        #
        #'Interfaces': dictionary {'Interface': dictionary
        #{'Status': string, 'Protocol': string, 'Description': string}}:
        #
        
        ID = {'Host':host}
        session = self.find_password(host,ID)
        self.collect_info(host, session, ID)
        session.disconnect()
        self.devices.append(ID)
        return ID

    def collect_info(self, host, session, ID):
        #in open session send command do get infor
        
        # Privilegied EXEC mode
        session.enable()
        interfaces = {}
        modules = {}
        
        #get OS version
        output = session.send_command('show version | inc Cisco')
        version = re.search ('(Version .*),',output)
        #get Hardware version
        hw_version = re.search ('Cisco\s*\d+', output)
        #get interface description
        output = session.send_command('show int descr')
        for line in output.splitlines():
            data = re.search('(.*\d) *(up|down|admin down) *(up|down) *(.*)', line)
            if data:
                interfaces[data.group(1)]= {}
                interfaces[data.group(1)]['Status']= data.group(2)
                interfaces[data.group(1)]['Protocol'] = data.group(3)
                interfaces[data.group(1)]['Description'] = data.group(4)
         
        #get modules
        output =  session.send_command('show diag')
        matches = re.findall('(Slot .*):\n\s*(.*)', output)
        if matches:
            for match in matches:
                modules [match[0]] = match[1]
        ID['Hardware version'] = hw_version.group(0)
        ID['Modules'] = modules
        ID['Interfaces'] = interfaces    
        ID['IOS version'] = version.group(1)

        # Get CDP neighbors and use regex
        output = session.send_command('show cdp neighbors')
        matches = re.finditer(r'(\S+)\s+\S+\s\d/\d\s+\d+', output, re.MULTILINE)

        # Add CDP neighbors into a list
        devicesCDP = list()
        for matchNum, match in enumerate(matches):
            for groupNum in range(0, len(match.groups())):
                devicesCDP.append(match.group(1))

        if len(devicesCDP) > 0:
            # Get Hostname and domain name by display running-config
            output = session.send_command('show run | section hostname')
            hostname = re.search ('hostname (.*)', output)

            output = session.send_command('show run | section ip domain name')
            domain_name = re.search ('ip domain name (.*)', output)

            # If the domain_name is set, take it into account
            if domain_name is not None:
                self.computeNeighbors(devicesCDP, str(hostname.group(1)) + '.' + str(domain_name.group(1)))
            else:
                # Take only the hostname if domain_name is not set
                self.computeNeighbors(devicesCDP, hostname.group(1))
        
        # Exit Privilegied EXEC mode
        session.exit_enable_mode()
        
        return ID

    """
    Method allowing to compute all the CDP neighbors
    """
    def computeNeighbors(self, devicesCDP, hostname):
        # Compute the neighbors and add them into a dictionnary
        self.neighbors[hostname] = list()
        for device in devicesCDP:
            self.neighbors[hostname].append(device);
