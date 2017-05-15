import os
import sys
import argparse
import cProfile
import bucket
import random
import tempfile
import db
from datetime import timedelta
from datetime import datetime, date, time
import pstats
import memory_profiler
import pprofile

ErrUsage = "usage"
ErrUnknownCommand = "unknow command"
ErrPathRequired = "path required"
ErrFileNotFound = "file not found"
ErrInvalidValue = "invalid file"
ErrCorrupt = "invalid value"
ErrNonDivisibleBatchSize = "number of iteration must be divisible by the batch size"
ErrPageIDRequired = "page id required"
ErrPageNotFound = "page not found"
ErrPageFreed = "page freed"

PageHeaderSize = 16
class Main(object):
    def __init__(self):
        self.stdin = sys.stdin
        self.stderr = sys.stderr
        self.stdout = sys.stdout
    def run(self,*args):
        if len(args) == 0 or args[0].startswith('-'):
            self.stderr.write(self.Usage())
            return ErrUsage
        if args[0] == 'help':
            self.stderr.write(self.Usage())
            return ErrUsage
        elif args[0] == "bench":
            return NewBenchCmd(self).Run(args[1:])
        elif args[0] == 'check':
            return ''
        elif args[0] == 'compact':
            return ''
        elif args[0] == 'dump':
            return ''
        elif args[0] == 'info':
            return ''
        elif args[0] == 'page':
            return  ''
        elif args[0] == 'pages':
            return ''
        elif args[0] == 'stats':
            return ''
        else:
            return ErrUnknownCommand

    def Usage(self):
        return '''Bolt is a tool for inspecting bolt databases.

                  Usage:

	                bolt command [arguments]
	                
                  The commands are:

                    bench       run synthetic benchmark against bolt
                    check       verifies integrity of bolt database
                    compact     copies a bolt database, compacting it in the process
                    info        print basic info
                    help        print this screen
                    pages       print list of pages with their types
                    stats       iterate over all pages and generate usage stats

                  Use "bolt [command] -h" for more information about a command.
                '''
class BenchOptions:
    def __init__(self,parser):
        self.ProfileMode = parser.ProfileMode
        self.WriteMode = parser.WriteMode
        self.ReadMode = parser.ReadMode
        self.Iterations = parser.Iterations
        self.BatchSize = parser.BatchSize
        self.KeySize = parser.KeySize
        self.ValueSize = parser.ValueSize
        self.CPUProfile = parser.CPUProfile
        self.MemProfile = parser.MemProfile
        self.BlockProfile = parser.BlockProfile
        self.StatsInterval = parser.StatsInterval
        self.FillPercent = parser.FillPercent
        self.NoSync = parser.NoSync
        self.Work = parser.Work
        self.Path = parser.Path

class BenchResult:
    def __init__(self):
        self.WriteOps = int()
        self.WriteDuration = timedelta()
        self.ReadOps = int()
        self.ReadDuration = timedelta()
    def WriteOpsDuration(self):
        if self.WriteOps is 0:
            return 0
        return self.WriteDuration / timedelta(microseconds=self.WriteOps)
    def WriteOpsPerSecond(self):
        op = self.WriteOpsDuration()
        if op is 0:
            return 0
        return int(timedelta.seconds) / int(self.ops)
    def ReadOpDuration(self):
        if self.ReadOps is 0:
            return 0
        return self.ReadDuration / timedelta(self.ReadOps)
    def ReadOpsPerSecond(self):
        op = self.ReadOpDuration()
        if op == 0:
            return 0
        return int(timedelta.seconds) / int(self.ops)

class BenchCmd:
    def __init__(self,Main):
        self.stdin = Main.stdin
        self.stdout = Main.stdout
        self.stderr = Main.stderr
        self.profile = cProfile.Profile()
        self.mem_profile = memory_profiler()
    def ParseFlags(self,*args):
        options = BenchOptions()
        parser = argparse.ArgumentParser()
        parser.add_argument("profile-mode",default='rw',help='',type=str)
        parser.add_argument("write-mode",default='seq',help='',type=str)
        parser.add_argument('read-mode',default='seq',help='',type=str)
        parser.add_argument('count',default=1000,type=int,help='')
        parser.add_argument('batch-size',default=0,type=int,help='')
        parser.add_argument('key-size',default=8,type=int,help='')
        parser.add_argument('value-size',default=32,type=int,help='')
        parser.add_argument('cpuprofile',default='',type=str,help='')
        parser.add_argument('memprofile',default='',type=str,help='')
        parser.add_argument('blockprofile',default='',type=str,help='')
        parser.add_argument('fill-percent',default=bucket.DefaultFillPercent,type=float,help='')
        parser.add_argument('no-sync',default=False,type=bool,help='')
        parser.add_argument('work',default=False,type=bool,help='')
        parser.add_argument('path',default='',type=str,help='')
        parser.parse_args(args=args)
        options = BenchOptions(parser)
        if options.BatchSize == 0:
            options.BatchSize = options.Iterations
        elif options.Iterations%options.BatchSize is not 0:
            return None , ErrNonDivisibleBatchSize
        if options.Path == '':
            f ,path = tempfile.mkstemp(suffix='bolt-bench-')
            options.Path = path
            f.close()
        return options, ''

    def Run(self,*args):
        options, err = self.ParseFlags(args)
        if err is not '':
            return err
        if options.Work:
            self.stdout.write('work: %s\n' % options.Path)
        else:
            os.remove(options.Path)
            '''heatate'''
        d, err = db.Open(options.Path,0666,None)
        if err is not '':
            return err
        d.NoSync = options.NoSync
        results = BenchResult()
        err = self.runWirtes(d, options, results )
        if err is not '':
            return 'bench: read: %s' % err
        self.stderr.write("# Write\t%v\t(%v/op)\t(%v op/sec)\n" % results.WriteDuration,results.WriteOpsDuration(),results.WriteOpsPerSecond())
        self.stderr.write("# Read\t%v\t(%v/op)\t(%v op/sec)\n" % results.ReadDuration, results.ReadOpDuration(), results.ReadOpsPerSecond())
        self.stderr.write("")
        return ''
    def runWrite(self,DB ,BenchOptions,BenchResult):
        if BenchOptions.ProfileMode is 'rw' and BenchOptions.ProfileMode is 'w':
            self.startProfiling(BenchOptions)
        t = datetime.now()
        if BenchOptions.WriteMode is 'seq':
            err = self.runWritesSequential(DB,BenchOptions,BenchResult)
        elif BenchOptions.WriteMode is 'rnd':
            err = self.runWritesRandom(DB,BenchOptions,BenchResult)
        elif BenchOptions.WriteMode is 'seq-nest':
            err = self.runWritesSequentialNested(DB,BenchOptions,BenchResult)
        elif BenchOptions.WriteMode is 'rnd-nest':
            err = self.runWritesRandomNested(DB,BenchOptions,BenchResult)
        else:
            return "invalid write mode: %s" % BenchOptions.WriteMode
        BenchResult.WriteDuration = datetime.now() - t

        if BenchOptions.ProfileMode is 'w':
            self.stopProfiling()
        return err
    def stopProfiling(self):
        if BenchOptions.CPUProfile is '':
            cpuprofile = open(BenchOptions.CPUProfile)
            if cpuprofile is None:
                self.stderr.write("bench: could not create cpu profile %q: %v\n" % BenchOptions.CPUProfile, err)
                os.exit(1)
            self.profile.disable()
            self.profile.dump_stats(cpuprofile)
    def startProfiling(self,BenchOptions):
        err = ''
        if BenchOptions.CPUProfile is not '':
            self.profile.enable()
        if BenchOptions.MemProfile is not '':




def NewBenchCmd(Main):
    return BenchCmd(Main)

def main():
    os.exit(1)
