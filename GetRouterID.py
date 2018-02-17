#TODO revise collected ifno
#TODO check why only one result is displeyed

"""
#Libs used: re, netmiko

"""
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException
import re

class GetRouterID:
    #need list of available hosts and list of passowrds
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
        for host in self.hosts:
            self.connect(host)
        return self.devices

    def connect(self, host):
        ID = {'Host':host}
        session = self.find_password(host,ID)
        self.collect_info(host, session, ID)
        session.disconnect()
        self.devices.append(ID)
        return ID

    def collect_info(self, host, session, ID):
        #in open session send command do get infor

        output = session.send_command('show version')
        version = re.search ('(Version .*),',output)
        output = session.send_command('show invento')
        inventory = re.search('(PID: *.),',output)
        ID['IOS version'] = version.group(1)
        ID['Inventory'] = inventory.group(1)

        output = session.send_command('show cdp neighbors')
        matches = re.finditer(r'(\S+)\s+\S+\s\d/\d\s+\d+', output, re.MULTILINE)

        devicesCDP = list()
        for matchNum, match in enumerate(matches):
            for groupNum in range(0, len(match.groups())):
                devicesCDP.append(match.group(1))

        if len(devicesCDP) > 0:
            # Privilegied EXEC mode
            session.enable()

            # Get Hostname and domain name by display running-config
            output = session.send_command('show run | section hostname')
            hostname = re.search ('hostname (.*)', output)

            output = session.send_command('show run | section ip domain name')
            domain_name = re.search ('ip domain name (.*)', output)

            session.exit_enable_mode()

            if domain_name is not None:
                self.computeNeighbors(devicesCDP, str(hostname.group(1)) + '.' + str(domain_name.group(1)))
            else:
                self.computeNeighbors(devicesCDP, hostname.group(1))

        return ID

    def computeNeighbors(self, devicesCDP, hostname):
        self.neighbors[hostname] = list()
        for dev in devicesCDP:
            self.neighbors[hostname].append(dev);
