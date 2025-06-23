import glob

IP = []

for file in glob.glob("../materials/config_files/*.log"):
    with open(file) as f:
        for cur_line in f:
            line_list = cur_line.strip().split(' ')
            if line_list[0] == 'ip' and line_list[1] == 'address':
                ip_address = line_list[2]
                netmask = line_list[3]
                IP.append((ip_address, netmask))
        f.close()

IP = list(set(IP))

for x in IP:
    print(x)