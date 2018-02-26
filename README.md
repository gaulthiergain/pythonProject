# Welcome to the pythonProject wiki!

This project has been implemented by Boriychuk Dima and Gain Gaulthier for the Cisco Incubator Program (2018). 

## Overview and objectives

The aim of this project is to build an automated solution to document the network environment. It must satisfy the following requirements:
1. All available devices in the network must be discovered. For each device, the following information must be obtained:
   * hardware version,
   * OS version running on the device,
   * management ip address,
   * password
   * modules which are installed on the device - and status of each module
2. The network topology must be viewable.
3. Interface description and interface status for each interface on each device must be printed.
4. The solution should be well documented and anyone should be able to run the solution and get up to date information.

## Architecture

The main file of the project is _script.py_. It allows to perform the following:
1. Read the file _range.txt_
2. Read the file _password.txt_
3. Ping all the devices that are active.
4. Connect to them and collect info.
5. Get info about End Of Life.
6. Output results into HTML file and show it.
7. Build the topology.

The file _PingObject.py_ allows to ping all active devices by using the broadcast address of the network. This last one is computed thanks to the _range.txt_ (which contains a IPv4 range in the following format: X.X.X.X/Y where X is byte of an IPv4 address and Y is the network mask). Note that the library _[ipaddress](https://docs.python.org/3/library/ipaddress.html)_ has been used to manipulate IP addresses.

The file _GetRouterID.py_ allows to connect to a router via SSH and to retrieve all the necessary data. To do that, the library _[netmiko](https://github.com/ktbyers/netmiko)_ was used. 

Then the file _HTMLoutput.py_ allows to print data into a local HTML file. 

Finally a 2D graph which represents the current topology of the network (built thanks to CDP neighbors) is printed thanks to the libraries _[networkx](https://networkx.github.io)_ and _[matplotlib](https://matplotlib.org)_.

## Running script

All project has been developed with *python 2.7.10*. To run the program, use the command: _python script.py_. 

Note that a _password_ and a _range_ files must been created before running the script otherwise an exception will occur. 
