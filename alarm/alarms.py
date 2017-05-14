import logging
import threading

alarmBucketName = str("alarm")
logging.basicConfig(
    level=logging.DEBUG,
    format='github.com/coreos/etcd  %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='/tmp/test.log',
    filemode='w')

class BackendGetter:
    def Backend(self):
        pass

alarmSet = {}

class AlarmStore:
    mu = threading.Lock()
    def __init__(self,bg):
        self.types = {}
        self.bg = bg
    def restore(self):
        b = BackendGetter(self.bg).Backend()
        tx = b.BatchTx()
        




