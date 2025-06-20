import ipaddress
import random

MIN_IP = 0x0B000000
MAX_IP = 0xDF000000

def comparable_ip_value(network):
    return int(network.netmask)*2**32 + int(network.network_address)

class IPv4RandomNetwork(ipaddress.IPv4Network):
    def regular(self):
        return self.is_global
    def random_net(self):
        net = random.randint(MIN_IP, MAX_IP)
        mask = random.randint(8, 24)
        return (net, mask)
    def __init__(self):
        net = self.random_net()
        ipaddress.IPv4Network.__init__(self, net, strict=False)

L = []
while len(L) < 50:
    generatedNet = IPv4RandomNetwork()
    if generatedNet.regular():
        L.append(generatedNet)

L.sort(key=comparable_ip_value)

for x in L:
    print(x)

# net = random.randint(MIN_IP, MAX_IP)
# print(net)
#
# mask = random.randint(8, 24)
# print(mask)
#
# net1 = ipaddress.IPv4Network((net, mask), strict=False)
# print(net1)
