from time import time
from math import sin

def get_values():
    #normally get sensor data here
    return dict(co=100*sin(time()*0.2)+100)