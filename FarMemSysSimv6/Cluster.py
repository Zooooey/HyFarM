from operator import truediv
import Task
import Server

class Cluster:
    nowTime = 0.0
    servers = [ ]
    runningTasks = { } # TaskId => Task()
    alias_mcelist = [ ]
    def __init__(self, serverList):
        self.nowTime = 0.0
        self.servers = serverList
        self.update_server_mce_list()

    def allocTask(self, task):
        self.runningTasks[task.id] = task
        self.servers[task.localServer].addTask(task.id, task,task.localMem)

    def allocWithFarTask(self, localTask, farTask):
        self.runningTasks[localTask.id] = localTask
        self.servers[localTask.localServer].addTask(localTask.id, localTask)
        mem = self.servers[farTask.localServer].localMem - farTask.localMem - localTask.hfm
        ssd = self.servers[farTask.localServer].ssd - farTask.ssd
        self.servers[farTask.localServer].resetTask(farTask.id, farTask, mem, ssd)

    def allocFarTask(self, task, farMem, localserver, farserver):
        task.updateFarServer(farMem,farserver)
        self.runningTask[task.id] = task.id
        self.servers[localserver.id].addTask(task.id,task, task.ocalMem)
        self.servers[farserver.id].addTask(task.id,task, task.localMem)

    def finishTask(self):
        if len(self.runningTasks) == 0:
            return False
        mintime = float('inf')
        for t in self.runningTasks.values():
            if t.runtime < mintime:
                task = t
                mintime = t.runtime
        self.nowTime = task.runtime
        self.servers[task.farServer].finishFarTask(task.hfm)
        self.servers[task.localServer].finishTask(task.id)
        del self.runningTasks[task.id]
        return True

    def update_server_mce_list(self):
        mcelist = [server.mce for server in self.servers]
        sum = 0
        for i in mcelist:
            sum= sum + i
        if(len(mcelist) == 0):
            average = 0
        else:
            average = sum / len(mcelist)
        self.alias_mcelist = [server.mce - average for server in self.servers]



