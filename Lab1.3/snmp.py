from pysnmp.hlapi import *

SNMP_VERSION = 1
COMMUNITY_NAME = 'public'
MIB_VERSION = 'SNMPv2-MIB/sysDescr'
MIB_INTERFACE_LIST = '1.3.6.1.2.1.2.2.1.2'

result = getCmd(SnmpEngine(),
                CommunityData(COMMUNITY_NAME, mpModel=0),
                UdpTransportTarget(('10.31.70.209', 161)),
                ContextData(),
                ObjectType(ObjectIdentity(MIB_VERSION.split('/')[0], MIB_VERSION.split('/')[1], 0)))

# print(type(result))

for x in result:
    for y in x[3]:
        print(y)

print('\n')

result = nextCmd(SnmpEngine(), CommunityData(COMMUNITY_NAME, mpModel=0),
                 UdpTransportTarget(('10.31.70.209', 161)),
                 ContextData(),
                 ObjectType(ObjectIdentity(MIB_INTERFACE_LIST)),
                 lexicographicMode=False)

for x in result:
    for y in x[3]:
        print(y)