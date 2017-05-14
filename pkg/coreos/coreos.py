import io
import os

def ReadFile(filename):
    isExist = os.path.exists(filename)
    if isExist == False:
        return "",False
    f = io.open(filename,'r')
    try:
        buf = f.read()
        return buf,True
    finally:
        f.close()
def IsCoreOS():
    buf , isExist = ReadFile("/usr/lib/os-release")
    if isExist:
        return str(buf)
    else:
        return False