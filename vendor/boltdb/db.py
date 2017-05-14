import platform
import os
import datetime
from datetime import timedelta
import resource
import io

maxMmapStep = 1 << 30
version = 2
magic = 0xED0CDAED
IgnoreNoSync = platform.system() is "openbsd"

DefaultMaxBatchSize = 1000
DefaultMaxBatchDelay = 10 * timedelta.microseconds
DefaultAllocSize = 16 * 1024 * 1024

defaultPageSize = resource.getpagesize()

class meta:
    magic = int()
    version = int()
    pageSize = int()
    flags = int()
    '''root = bucket()'''
    freelist = int()
    pgid = int()
    txid = int()
    checksum = int()

class DB:
    StrictMode = bool()
    NoSync = bool()
    MmapFlags = int()
    MaxBatchSize = int()
    MaxBatchDelay = datetime.timedelta()
    AllocSize = int()
    path = str()
    file = io.FileIO()
    lockfile = io.FileIO()
    dataref = bytes()
    data = {}
    datasz = int()
    filesz = int()


