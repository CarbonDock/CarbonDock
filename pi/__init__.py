import sys,os
os.chdir('/home/pi/Desktop/node')
from p2p import Node, getIp
from envirobox import get_values
from socket import *
from time import sleep
import gpiozero
from threading import Thread

print('init...')
print(getIp())

def get_status(kwargs):
    co = int(get_values()['co'])
    print(co)
    danger_value = 1.306837 + (0.02774721 - 1.306837)/(1 + (co/128.288)**2.844361)
    
    if danger_value <= 0.1:
        stat = 'Safe.'
    elif danger_value <= 0.25:
        stat = 'Slightly risky.'
    elif danger_value <= 0.4:
        stat = 'At risk.'
    elif danger_value <= 0.7:
        stat = 'Dangerous'
    else:
        stat = 'Leave.'

    return {'danger_coeff':danger_value,'danger':stat}

def ledUpdateLoop():
    RED = gpiozero.PWMLED(2)
    GREEN = gpiozero.PWMLED(0)
    while True:
        stat = get_status({})['danger_coeff']
        RED.value = stat
        GREEN.value = 1.0-stat
        sleep(0.1)

if __name__ == '__main__':
    t = Thread(target=ledUpdateLoop)
    t.start()
    node = Node(6767,6768,'CarbonDock-'+getIp(),protocol='CarbonDock',status=get_status)
        

