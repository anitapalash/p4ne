import paramiko, time, requests
from pprint import pprint

# Инструмент jupyter - изучить

BUF_SIZE = 50000
TIMEOUT = 1

ssh_connection = paramiko.SSHClient()
ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connection.connect(hostname='10.31.70.209', username='restapi', password='j0sg1280-7@')
session = ssh_connection.invoke_shell()

session.send("\n\n\n".encode())
time.sleep(2)
session.send("\nterminal length 0\n\n\n".encode())
time.sleep(2)
session.send("\n\nshow run\n\n".encode())
time.sleep(1)
buf = session.recv(BUF_SIZE)
print(buf.decode())

ssh_connection.close()

headers = { 'accept': 'application/yang-data+json', 'Content-type': 'application/yang-data+json'}
r = requests.get('https://10.31.70.209/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces', headers=headers,
                 verify=False, auth=('restapi', 'j0sg1280-7@'))
pprint(r.json(), indent=4)


