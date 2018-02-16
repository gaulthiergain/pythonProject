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
        self.ID = {}
        self.devices = []
    
    def connect(self):
    #in loop use all IP find our correct password and collect info from router
        for host in self.hosts:
            print 'connection to', host
            for password in self.passwords:
                    try:
                        session = ConnectHandler(device_type = 'cisco_ios',
                                                 ip = host, 
                                                 username = 'admin', 
                                                 password = password)
                        check = session.is_alive()
                        print check
                        self.ID['Host'] = host
                        self.ID['Password'] = password
                        self.collect_info(session)                
                        session.disconnect()
                        check = session.is_alive()
                        print check
                        self.devices.append(self.ID)
                    except NetMikoAuthenticationException:
                        continue
        return self.devices

    def collect_info(self,session):
    #in open session send command do get infor
        output = session.send_command('show version')
        version = re.search ('(Version .*),',output)
        output = session.send_command('show invento')
        inventory = re.search('(PID: *.),',output)
        self.ID['IOS version'] = version.group(1)
        self.ID['Inventory'] = inventory.group(1)
        
      

