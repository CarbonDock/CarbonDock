import sys,os
sys.path.insert(1,os.path.join('..'))
print([os.path.abspath(i) for i in sys.path])
import carbonp2p
from envirobox import get_values
from socket import *
from http.server import HTTPServer, SimpleHTTPRequestHandler
from json import dump

class Handler(SimpleHTTPRequestHandler):
    def send_head(self,path=None):
        #modified from http.server
        if not path:
            path = self.translate_path(self.path)
        try:
            f = open(path, 'rb')

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise
    def do_GET(self):
        with open('resp.json','w') as f:
            x = int(get_values()['co'])
            dump(dict(
                danger = 1.306837 + (0.02774721 - 1.306837)/(1 + (x/128.288)**2.844361)
            ),f)
        f = self.send_head(path='resp.json')
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()


if __name__ == '__main__':
    Node = carbonp2p.Node(6767,6768,'CarbonDock-'+gethostbyname(gethostname()),protocol='CarbonDock')
    
        

