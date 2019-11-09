from time import time
from math import sin

def get_values():
    #normally get sensor data here
    return dict(co=3*sin(time()*0.1)+3)