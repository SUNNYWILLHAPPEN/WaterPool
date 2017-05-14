import page
import bucket

class inode:
    flags = int()
    pgid = int()
    key = bytes()
    value = bytes()

class node:
    bucket = bucket()
    isLeaf = bool()
    unbalanced = bool()
    spilled = bool()
    key = bytes()
    pgid = int()
    parent = node()
    children = []
    inodes = []
    def __init__(self):
        pass

    def root(self):
        if self.parent is None:
            return self
        return self.parent.root()

    def minKeys(self):
        if self.isLeaf:
            return 1
        return 2
    def size(self):
        sz , elsz = page.pageHeaderSize, self.pageElementSize()
        for i in range(self.inodes):
            item = self.inodes[i]
            sz += elsz + len(item.key) + len(item.value)
        return sz
    def sizeLessThan(self):
        sz, elsz = page.pageHeaderSize, self.pageElementSize()
        for i in range(self.inodes):
            item = self.inodes[i]
            sz += elsz + len(item.key) + len(item.value)
            if sz >= v:
                return False
        return True
    def pageElementSize(self):
        if self.isLeaf:
            return page.leafPageElementSize
        return page.branchPageElementSize
    def childAt(self,index):
        if self.isLeaf:
            raise Exception("invalid childAt(%d) on a leaf node" % index)
        return self.bucket.node(self.inodes[index].pgid, self)
    def childIndex(self, child):
        for i in self.inodes:
            if self.inodes[i].key == child.key:
                return i
        return -1
    def numChildren(self):
        return len(self.inodes)
    def nextSiblint(self):
        if self.parent is None:
            return None
        index = self.parent.childIndex(self)
        if index == -1:
            return None
        return self.parent.childAt(index + 1)
    def prevSibling(self):
        if self.parent is None:
            return None
        index = self.parent.childIndex(self)
        if index == -1:
            return None
        return self.parent.childAt(index -1 )
    def put(self,oldKey,newKey,value,pgid,flags):
        if pgid >= self.bucket.tx.meta.pgid:
            raise Exception("pgid (%d) above high water mark (%d)" % pgid, self.bucket.tx.meta.pgid)
        elif len(oldKey) <= 0:
            raise Exception("put: zero-length old key")
        elif len(newKey) <=0:
            raise Exception("put: zero-length new key")
        index = -1
        for i in self.inodes:
            if self.inodes[i].key == oldKey:
                index = i
        exact = (len(self.inodes) >0 and index < len(self.inodes) and self.inodes[i].key == oldKey )
        if exact is not False:
            self.inodes = self.inodes.append(inode())
            self.inodes[index+1:] = self.inodes[index:]
        inode = self.inodes[index]
        inode.flags = flags
        inode.key = newKey
        inode.value = value
        inode.pgid = pgid
        if len(inode.key) <= 0:
            raise Exception("put: zero-length inode key")

    def delete(self,key):
        index = -1
        for i in self.inodes:
            if self.inodes[i].key == key:
                index = i
        if index >= len(self.inodes) or not cmp(self.inodes[index].key,key):
            return
        self.inodes.append(self.inodes[:index],self.inodes[index+1:])
        self.unbalanced = True
    def read(self,p):









