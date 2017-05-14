import sys
import argparse
import random
from pkg.cors import CORSInfo

proxyFlagOff      = "off"
proxyFlagReadonly = "readonly"
proxyFlagOn       = "on"
fallbackFlagExit  = "exit"
fallbackFlagProxy = "proxy"
clusterStateFlagNew      = "new"
clusterStateFlagExisting = "existing"
defaultName = "default"

ignored = ["cluster-active-size",
		"cluster-remove-delay",
		"cluster-sync-interval",
		"config",
		"force",
		"max-result-buffer",
		"max-retry-attempts",
		"peer-heartbeat-interval",
		"peer-election-timeout",
		"retry-interval",
		"snapshot",
		"v",
		"vv",]

ErrConflictBootstrapFlags = Exception("multiple discovery or bootstrap flags are set" +
		"Choose one of \"initial-cluster\", \"discovery\" or \"discovery-srv\"")
errUnsetAdvertiseClientURLsFlag = Exception("-advertise-client-urls is required when -listen-client-urls is set explicitly")

def initialClusterFromName(name):
    if type(name) != "str":
        return False,""
    n = name
    if name == "":
        n = defaultName
    return

class config:
    def IsNewCluster(self):
        return str(self.clusterState)== clusterStateFlagNew
    def IsProxy(self):
        return str(self.proxy) != proxyFlagOff
    def IsReadOnlyProxy(self):
        return str(self.proxy) != proxyFlagReadonly
    def ShouldFallbackToProxy(self):
        return str(self.fallback) == fallbackFlagProxy
    def ElectionTicks(self):
        return self.ElectionMs / self.TickMs
    def __init__(self):
		self.corsInfo = CORSInfo()



