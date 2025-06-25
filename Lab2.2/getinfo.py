from flask import Flask, render_template
import re, ipaddress, glob, re

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

if __name__ == '__main__':
    app.run(debug=True)