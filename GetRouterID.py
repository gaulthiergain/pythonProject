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
        
    def find_password(self, host, ID):
        for password in self.passwords:
            try:
                session = ConnectHandler(device_type = 'cisco_ios',
                                         ip = host, 
                                         username = 'admin', 
                                         password = password)
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
        self.collect_info(session, ID)
        session.disconnect()
        self.devices.append(ID)
        return ID

    def collect_info(self,session, ID):
    #in open session send command do get infor
        output = session.send_command('show version')
        version = re.search ('(Version .*),',output)
        output = session.send_command('show invento')
        inventory = re.search('(PID: *.),',output)
        ID['IOS version'] = version.group(1)
        ID['Inventory'] = inventory.group(1)
        return ID
        
      

