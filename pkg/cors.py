import string
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler


class CORSInfo:
    def __init__(self):
        self.data = {}
    def Set(self,s):
       m = {}
       ss = string.strip(s,",")
       for v in ss:
           v = string.strip(v,' ')
           if v == "":
              continue
           if v != "*":
              res = urlparse.urlparse(v)
              m[v] = True
       data = m

    def String(self):
        o = []
        for k,_ in self.data:
            o = o.append(k)

    def OriginAllowed(self,origin):
            return self.data["*"] or self.data[origin]

class CORSHandler(BaseHTTPRequestHandler):
    StatusOK = 200
    def __init__(self):
        self.Info = CORSInfo()
    def addHeader(self,origin):
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Headers", "accept, content-type")
    def handlers(self):
        origin = self.headers.getheaders("Origin")
        if self.Info.OriginAllowed("*"):
            self.addHeader("*")
        elif self.Info.OriginAllowed(origin):
            self.addHeader(origin)
    def do_GET(self):
        self.handlers()
        self.end_headers()
    def do_POST(self):
        self.handlers()
        self.end_headers()
    def do_OPTIONS(self):
        self.handlers()
        self.send_response(self.StatusOK)
    """def ServerHttp(self,w Re):"""
