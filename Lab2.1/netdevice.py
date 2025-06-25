import paramiko, time, requests, re

PASSWORD = 'j0sg1280-7@'
USERNAME = 'restapi'
HOSTNAME = '10.31.70.209'
BUF_SIZE = 50000
TIMEOUT = 1

print("Interfaces by paramiko")

ssh_connection = paramiko.SSHClient()
ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_connection.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)
session = ssh_connection.invoke_shell()

session.send("\n".encode())
time.sleep(2)
session.send("\nterminal length 0\n".encode())
time.sleep(2)
session.send("\nshow interface\n".encode())
time.sleep(2)
result = session.recv(BUF_SIZE).decode()

for line in re.finditer("((Internet address is )([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))|(([0-9]+ packets )(input|output), [0-9]+ bytes)", result):
    print(line.group(0))

ssh_connection.close()

headers = { 'accept': 'application/yang-data+json', 'Content-type': 'application/yang-data+json'}
r = requests.get('https://10.31.70.209/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces', headers=headers,
                 verify=False, auth=(USERNAME, PASSWORD))
# pprint(r.json())
print("Interfaces by REST")

for interface in r.json()['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
    ip4v = interface['ipv4']
    ip4v_mask = interface['ipv4-subnet-mask']
    accepted_packets = interface['v4-protocol-stats']['in-pkts']
    accepted_bytes = interface['v4-protocol-stats']['in-octets']
    out_packets = interface['v4-protocol-stats']['out-pkts']
    out_bytes = interface['v4-protocol-stats']['out-octets']
    print(f'IP: {ip4v}\n Mask: {ip4v_mask}\n Accepted packets: {accepted_packets}\n Output packets: {out_packets} \n Accepted Bytes: {accepted_bytes}\n Output Bytes: {out_bytes}\n***')
