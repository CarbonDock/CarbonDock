from __future__ import print_function	# For Py2/3 compatibility
import eel
from time import time
from socket import *

# Set web files folder
eel.init('web')

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
    
    return ret[1],ret[2]

@eel.expose
def ips():


eel.start('index.html', size=(300, 200))    # Start
