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
    leastlocalratio = 10 # 定义任务所需的最小内存比例，由这个比例确定，10代表10/10，即leastLocalMemory = 10/10的localMemory
    leastlocalmemory = 0 # task所需的最小localMemory
    type = 0
    fixed_mce = 0
    mce = 0.0
    localServer = 0
    localMem = 0.0 # 当前所在的server里，这个task使用这个server的localMem
    farServer = 0
    hfm = 0.0
    ssd = 0.0
    runtime = 0.0

    def __init__(self, id, memory, latencylist, pagefaultlist, SLA):
        """

        :param id:
        :param memory: 该任务需要消耗的内存(本地和远程都需要)
        :param latencylist:有10个，第一个是shortestLatency
        :param pagefaultlist:
        :param SLA: SLA和最小的latency相乘得到accept_latency，利用accept_latency算出leastlocalratio。例如: latencyList=[1,2,...10]
        SLA=3，那么accept_latency=1*3 = 3, 那么latency列表里只有3个latency小于3。由此求得leastlocalratio=10-3+1 = 8;
        """
        self.id = id
        self.memory = memory
        self.localMem = 0
        self.latencylist = latencylist
        self.pagefaultlist = pagefaultlist
        self.shortestLatancy = latencylist[0]
        self.leastlocalratio = self.get_least_local_ratio(SLA)
        #self.leastlocalratio = leastlocalratio
        # 根据SLA求得leastlocalratio后，可以定位再latenclist列表里最长的latency，超过这个latency视为不能接受。
        self.longestLatancy = latencylist[10 - self.leastlocalratio]
        # 求得leastlocalratio后利用它求本task至少要留多少local mem
        self.leastlocalmemory = self.leastlocalratio/10 * memory
        #self.profile = profile
        # fixed_mce在这里的含义是当前task多少内存可以存放到远端
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
        if self.farMem>0: # FIXME: 原作者并没有实现farMem的相关功能，所以这个if不会成功
            self.mce = self.localMem - self.leastlocalratio/10 * self.memory + self.farMem
            self.hfm = min(self.farMem, self.memory-self.localMem)
        else:
            # self.localMem是当前task在当前server上使用的本地内存大小，减去的是当前task至少需要的本地内存数。他们的差值含义就是还有多少内存可以evict出去。
            self.mce = self.localMem - self.leastlocalratio / 10 * self.memory
            self.hfm = 0.0

    def updateFarServer(self, farMem, farserver):
        self.localMem = self.localMem - farMem
        self.hfm = farMem
        self.farServer = farserver
        self.ssd = self.memory - self.localMem - self.hfm

    def get_least_local_ratio(self, SLA):
        """
        least local ratio需要靠SLA来计算。假设一个latency list = [1,2,3,...10]，SLA=4。
        那么shortest latency = 1；accept latency = 4 * shortest latency = 4；
        那么这个list里能被接受的latency只有4个，所以least local ratio = 10 - 4 +1 = 7；
        :param SLA:
        :return:
        """
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