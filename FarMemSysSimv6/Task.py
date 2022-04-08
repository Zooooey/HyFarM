from email.mime import base
from numpy import polyfit, poly1d

class Task:
    id = 0
    memory = 0.0  #M
    shortestLatancy = 0.0
    longestLatancy = 0.0
    profile = {0.0 : (0.0, 0.0)}  #farRatio => (latancy, page fault)  latency =>far ratio, page fault
    pagefaultlist = [0] * 11 #far ratio = 0,1,2,3,4,5,6,7,8,9,10
    latencylist = [0.0] * 11 #far ratio = 0,1,2,3,4,5,6,7,8,9,10
    leastlocalratio = 10
    leastlocalmemory = 0
    type = 0
    fixed_mce = 0
    mce = 0.0
    localServer = 0
    localMem = 0.0
    farServer = 0
    hfm = 0.0
    ssd = 0.0
    runtime = 0.0

    def __init__(self, id, memory, latencylist, pagefaultlist, SLA):
        self.id = id
        self.memory = memory
        self.localMem = 0
        self.latencylist = latencylist
        self.pagefaultlist = pagefaultlist
        self.shortestLatancy = latencylist[0]
        self.leastlocalratio = self.get_least_local_ratio(SLA)
        #self.leastlocalratio = leastlocalratio
        self.longestLatancy = latencylist[10 - self.leastlocalratio]
        self.leastlocalmemory = self.leastlocalratio/10 * memory
        #self.profile = profile
        self.fixed_mce = self.memory - self.leastlocalratio/10 * self.memory
        self.hfm = 0.0
        self.ssd = self.memory-self.localMem-self.hfm
        self.runtime = 0.0
        self.mce = 0.0
        self.localServer = 0
        self.farServer = 0
        self.farMem = 0

    def setRunInfo(self, serverId, mem, farServerId, hfm, ssd, basetime):
        self.localServer = serverId
        self.localMem = mem
        self.farServer = farServerId
        self.hfm = hfm
        self.ssd = ssd
        self.updateRuntime(basetime)

    def updateID(self, id):
        self.id = id

    #TODO
    def updateRuntime(self, basetime):
        self.runtime = basetime
        self.runtime += 0.0

    def updateMem(self, localMem ):
        self.localMem = localMem
        self.ssd = self.memory - self.localMem - self.hfm


    def updateMCE(self):
        #self.mce = (10 -self.leastlocalratio)/10 * self.memory
        if self.farMem>0:
            self.mce = self.localMem - self.leastlocalratio/10 * self.memory + self.farMem
            self.hfm = min(self.farMem, self.memory-self.localMem)
        else:
            self.mce = self.localMem - self.leastlocalratio / 10 * self.memory
            self.hfm = 0.0

    def updateFarServer(self, farMem, farserver):
        self.localMem = self.localMem - farMem
        self.hfm = farMem
        self.farServer = farserver
        self.ssd = self.memory - self.localMem - self.hfm

    def get_least_local_ratio(self, SLA):
        self.SLA = SLA
        accept_latency = SLA * self.shortestLatancy
        #print('accept_latency is ' + str(accept_latency))
        i = 0
        for la in self.latencylist:
            #print('la is ' +str(la))
            if la <= accept_latency:
                i = i+1
            else:
                break
        self.leastlocalratio = 10 -i+1
        print('task'+ repr(self.id) +' least_local_ratio is' + repr(self.leastlocalratio))
        return self.leastlocalratio


    def estimate_latency_by_profile(self):
        if self.localMem > self.leastlocalmemory :
            localratio:int =  int(self.localMem/self.memory *10)
        else:
            localratio:int = int(self.leastlocalmemory)
        #farratio:float = 10.0-localratio
        print('localratio in estimate: ' + repr(localratio))
        farratio_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        #latency_coeff = polyfit(farratio_index, self.latencylist, 6)
        #f = poly1d(latency_coeff)
        #est_latency = f(10-localratio)
        #est_latency = self.latencylist[self.leastlocalratio]#
        est_latency = self.latencylist[10-localratio]
        pagefault_coeff = polyfit(farratio_index, self.pagefaultlist, 6)
        hfm_ratio:float = (self.hfm+self.localMem)/self.memory *10
        f_p = poly1d(pagefault_coeff)
        difference = f_p(10.0-localratio) - f_p(10.0-hfm_ratio)
        #hfm_page = self.pagefaultlist[localratio] - self.pagefaultlist[hfm_ratio
        #est_latency = est_latency - difference*0.0002

        print('latency in estimate: ' + repr(est_latency))
        return est_latency


    def estimate_latency_by_pagefault(self, local_pages, hfm_pages):
        latency_per_SSD_page = (self.longestLatancy-self.shortestLatancy)/ (self.memory*250)
        latency_per_hfm_page = 0.2*latency_per_SSD_page
        latency_per_local_page = 0.1*latency_per_SSD_page
        est_latency = self.shortestLatancy +\
                      latency_per_hfm_page*hfm_pages +\
                      latency_per_SSD_page *((self.memory*250) - local_pages - hfm_pages)
        return est_latency