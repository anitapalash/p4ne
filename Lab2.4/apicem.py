import requests, pprint, ipaddress, glob, re
from flask import Flask, render_template

PASSWORD = 'j0sg1280-7@'
USERNAME = 'restapi'
HOSTNAME = '10.31.70.209'

def topProcesses():
    headers = {'accept': 'application/yang-data+json', 'Content-type': 'application/yang-data+json'}
    r = requests.get('https://10.31.70.209/restconf/data/Cisco-IOS-XE-process-memory-oper:memory-usage-processes',
                     headers=headers,
                     verify=False, auth=(USERNAME, PASSWORD))
    # pprint.pprint(r.json())

    print("Top-10 memory usage processes:")

    PROCESSES = []

    for process in r.json()['Cisco-IOS-XE-process-memory-oper:memory-usage-processes']['memory-usage-process']:
        allocated_memory = process['allocated-memory']
        name = process['name']
        pid = process['pid']
        PROCESSES.append({'name': name, 'allocated_memory': allocated_memory, 'pid': pid})

    PROCESSES.sort(key=lambda p: p['allocated_memory'], reverse=True)

    for i in range(0, 10):
        print(f'''Process with name {PROCESSES[i]["name"]}, pid {PROCESSES[i]["pid"]}
              allocated memory {PROCESSES[i]["allocated_memory"]}
        ''')

    return PROCESSES

def extract_ip(line):
    if re.match('^ ip address ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$', line):
        line_list = line.strip().split(' ')
        ip_address = line_list[2]
        netmask = line_list[3]
        return ipaddress.IPv4Interface((ip_address, netmask)).network
    else: return None

HOSTS = {}
for file in glob.glob('../materials/config_files/*.log'):
    with open(file) as f:
        IP = []
        for l in f:
            ip_int = extract_ip(l)
            if ip_int is not None:
                IP.append(ip_int)

        IP = sorted(list(set(IP)))
        hostname = re.findall('([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', file.__str__())[0]
        HOSTS[hostname] = IP

        f.close()


app = Flask(__name__)
@app.route('/')
def index():
    return "Hello, World!"

@app.route('/configs')
def configs():
    return render_template('templ.html', title='Configs', items=list(HOSTS.keys()))

@app.route('/config/<hostname>')
def host(hostname):
    return render_template('templ.html', title='Hosts', items=list(HOSTS[hostname]))

@app.route('/configs/processes')
def processes():
    return render_template('processes.html',
                           title='Top-10 memory usage processes:',
                           items=topProcesses()[0:10])

if __name__ == '__main__':
    app.run(debug=True)
