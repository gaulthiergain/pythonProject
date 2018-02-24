"""
#Libs used: webbrowser, os
"""
import webbrowser
import os

class HTML:
    # Need list of available hosts and list of passwords
    def __init__ (self, dev, EoL):
        self.dev = dev
        self.EoL = EoL

    def createHTML(self):
        web = open ('results.html','w')
        text = ' <!DOCTYPE html><html><head>'
        text +='<style>#customers {    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;'
        text +='    border-collapse: collapse;'
        text +='    width: 100%;}'
        text +='#customers td, #customers th {'
        text +='    border: 1px solid #ddd;'
        text +='    padding: 8px;}'
        text +='#customers tr:nth-child(even){background-color: #f2f2f2;}'
        text +='#customers tr:hover {background-color: #ddd;}'
        text +='#customers th {'
        text +='    padding-top: 12px;'
        text +='    padding-bottom: 12px;'
        text +='    text-align: left;'
        text +='    background-color: #4CAF50;'
        text +='    color: white;}</style>'
        text += '<meta charset="UTF-8"><title>Network details</title></head><body>'
        print web.closed
        web.write(text)
        for device in self.dev:
            text = '<h3> Router - host: ' + device['Host'] + '</h3> <table id="customers">'
            text += '<tr><td> IP </td> <td>' + device['Host'] + '</td></tr>'
            text += '<tr><td> Password </td> <td>' + device['Password'] + '</td></tr>'
            text += '<tr><td> Hardware version </td> <td>' + device['Hardware version'] + '</td></tr>'
            text += '<tr><td> OS version </td> <td>' + device['IOS version'] + '</td></tr>'
            text += '<tr><td> Serial numbers </td> <td>' + device['SN'] + '</td></tr></tr>'
            text += '</table></body></html>'
            text += '<p> Modules </p><table id="customers">'
            for slot, value in device['Modules'].items():
                text += '<tr><td>' + slot + '</td><td>' + value + '</td></tr>'
            text += '</table><br>'
            text += '<p> Interfaces </p><table id="customers">'
            for interface, info in device['Interfaces'].items():
                text += '<tr><th>' + interface + '</th><th>Status</th><th>Protocol</th><th>Description</th>'
                text += '<tr><td></td><td>'+ info['Status'] + '</td><td>' + info['Protocol'] + '</td><td>' + info['Description'] +'</td></tr>'
            text += '</table><br>'    
            web.write(text)
        text += '<h3> Last date of support for devises</h3>'
        text += '<table id="customers"><tr><th>Serial number</th><th>End of life date</th><tr>'
        for SN, date in self.EoL.items():
            text += '<tr><td>'+SN+'</td><td>'+date+'</td><tr>'
        text += '</table>'
        
        web.write(text)
        web.close()
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = 'file://' + dir_path + '/results.html'
        webbrowser.open_new_tab(filename)  
    