#!/usr/bin/python3
# Move to zabbix.conf or zabbix_proxy.conf $ExternalScripts
# chown zabbix.zabbix snmpv2-arp.py 
# chmod +x snmpv2-arp.py

import argparse
import sys
import re
import json  

from easysnmp import Session

result = {"data": []}     
def snmp_interface_discovery(system_items, oid):
    value = {}
    for item in system_items:
        ifId = item.oid_index
        value[ifId] = item.value
    return(value)    

def parse_complicated_index(system_items, oid):
    arpData = {}
    for item in system_items:
        ifId = item.oid_index.split('.')[0]
        ip = '.'.join(item.oid_index.split('.')[1:])
        arpData.update({ip: ifId}) 
    return(arpData)

def run_arp_snmp(host, community, port, oid, arpIfName,arpIfAlias):
    session = Session(hostname=host, community=community, remote_port = port, version=2, use_sprint_value=True)
    system_items = session.walk(oid)
    if oid == '1.3.6.1.2.1.4.22.1.2':
        snmpResult = []
        arpData = parse_complicated_index(system_items, oid)
        value1 = []
        value2 = []
        for ip in arpData.keys():
            data = {"{#ARPINDEX}": arpData[ip] + '.' + ip, "{#ARPIFNAME}": arpIfName[arpData[ip]], "{#ARPIP}": ip}
            snmpResult += [data]
    else:
        snmpResult = snmp_interface_discovery(system_items, oid)
    return(snmpResult)

                  

parser = argparse.ArgumentParser(description = 'This program create LLD SNMP discovery to get IP to MAC mapping for specific interface\n\tExample: snmpv2-arp.py 10.1.1.1 1.3.6.1.2.1.4.22.1.2')
parser.add_argument('host', metavar = 'host', type=str, help = 'SNMP host ip address or name')
parser.add_argument('oid', metavar = 'oid', type=str,help = 'SNMP oid')
parser.add_argument('--community', metavar = 'community', type=str,help = 'SNMP community string', default='public')
parser.add_argument('--port', metavar = 'port', type=str, help = 'SNMP port', default='161')
args = parser.parse_args()
arpIfName = {}
arpIfAlias = {}

arpIfName = run_arp_snmp(host = args.host, community = args.community, oid = '1.3.6.1.2.1.31.1.1.1.1', port = args.port, arpIfName = arpIfName, arpIfAlias = arpIfAlias) #ARPIFNAME
arpData = run_arp_snmp(host = args.host, community = args.community, oid = args.oid, port = args.port, arpIfName = arpIfName, arpIfAlias = arpIfAlias)

result["data"] += arpData
json_object = json.dumps(result)  
print(json_object) 


