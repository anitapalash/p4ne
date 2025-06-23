import re
import ipaddress
import glob

def extract_ip(line):
    if re.match('^ ip address ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$', line):
        line_list = line.strip().split(' ')
        ip_address = line_list[2]
        netmask = line_list[3]
        return ipaddress.IPv4Interface((ip_address, netmask))
    else: return None

IP = []
for file in glob.glob('../materials/config_files/*.log'):
    with open(file) as f:
        for l in f:
            ip_int = extract_ip(l)
            if ip_int is not None:
                IP.append(ip_int)
        f.close()

IP = sorted(list(set(IP)))
for ip in IP:
    print(ip)