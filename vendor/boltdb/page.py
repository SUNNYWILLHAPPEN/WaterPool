
pageHeaderSize = int()
minKeysPerPage = 2
branchPageElementSize = int()
leafPageElementSize = int()

brancPageFlag = 0x01
leafPageFlag = 0x02
metaPageFlag = 0x04
freeListPageFlag = 0x10
bucketLeafFlag = 0x01

class page:
    id = int()
    flag = int()
    count = int()
    overflow = int()
    ptr = id(None)