import sys
import tx
import page

MaxKeySize = 32768
MaxValueSize = (1 << 31) - 2
maxUint = 0
maxInt = ~int(0) & 0xffffffff
minInt = ~maxInt -1
DefaultFillPercent = 0.5
class bucket:
    root = int()
    sequence = int()

class Bucket:
    bucket = bucket()
    tx = tx.Tx()
    bucket = {}
    page = page.page()


bucketHeaderSize = int(sys.getsizeof(bucket()))

def newBucket():
    pass




