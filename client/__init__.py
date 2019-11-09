from __future__ import print_function	# For Py2/3 compatibility
from time import time
from socket import *

def discover(port,timeout=5):
    s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('', port))
    curtime = time()
    ret = {}
    while time() < curtime+timeout:
        data, addr = s.recvfrom(1024) #wait for a packet
        data = str(data)[2:].strip("'")
        if data.startswith('CarbonDock'):
            data = data.split('|')
            ret[data[1]] = data[2]
    ret2 = []
    for i in ret.keys():
        ret2.append([i,ret[i].split(':')[0]])
    print(ret2)
    return ret2

