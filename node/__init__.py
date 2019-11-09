import sys,os
sys.path.insert(1,os.path.join('..'))
#print([os.path.abspath(i) for i in sys.path])
import carbonp2p
from envirobox import get_values
from socket import *
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        pass


if __name__ == '__main__':
    Node = carbonp2p.Node(6767,6768,'CarbonDock-'+gethostbyname(gethostname()),protocol='CarbonDock')
    
        

