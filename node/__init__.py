import sys,os
sys.path.insert(1,os.path.join('..'))
from p2p import Node
from envirobox import get_values
from socket import *

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

if __name__ == '__main__':
    node = Node(6767,6768,'CarbonDock-'+gethostbyname(gethostname()),protocol='CarbonDock',status=get_status)
        

