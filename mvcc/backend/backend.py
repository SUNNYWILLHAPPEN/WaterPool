import time
import datetime
from datetime import timedelta
import threading
import logging

defaultBatchLimit = 10000
defaultBatchInterval = 100 * timedelta.microseconds
defragLimit = 10000
initialMmapSize = 10 * 1024 * 1024 * 1024
logging.basicConfig(
    format='github.com/coreos/etcd mvcc/backend %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='/tmp/test.log',
    filemode='w'
)
class Backend:
    def ReadTx(self):
        pass
    def BatchTx(self):
        pass
    def Snapshop(self):
        pass
    def Hash(self,ignores):
        pass
    def Size(self):
        pass
    def Defrag(self):
        pass
    def ForceCommit(self):
        pass
    def Close(self):
        pass

class Snapshot:
    def Size(self):
        pass
    def WriteTo(self):
        pass
    def Close(self):
        pass

class backend:
    size = int()
    commits = int()
    mu = threading.Lock()
    db 

