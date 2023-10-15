import Task
MAX_MEMORY = 20000
MAX_SSD = 2000000
class Server:
    #Server id
    id = 0

    # Available memory for this server
    localMem = MAX_MEMORY  #avalible Memory

    #farMem = 0
    farMemSever = 0
    ssd = MAX_MEMORY  #avalible SSD

    server_runningTasks = []  #taskId => Task()
    #TODO:what is mce?
    mce = 0.0
    least_mce_task = 0
    task_mce_list = [0.0]
    alias_task_mce_list = []

    def __init__(self, id, memory, ssd):
        self.id = id
        self.localMem = memory
        self.ssd = ssd
        self.mce = memory
        self.server_runningTasks = []
        self.least_mce_task = 0
        self.task_mce_list  = [0.0]
        self.alias_task_mce_list = []
        self.farMem = 0
        self.farMemSever = 0

    # append task instance into array 'server_runningTasks'

    def addTask(self, task, taskMem):
        self.server_runningTasks.append(task)
        task.localServer = self.id
        #task.updateMem(taskMem)
        if self.localMem >0 :
            self.localMem = self.localMem -taskMem
            self.ssd = self.ssd - task.ssd
        else:
            print("server " + repr(self.id) +" has no space" )
        #task.updateMCE()
        self.updateMCE()

    def resetTask(self, taskId, task, memory, ssd):
        self.server_runningTasks[taskId] = task
        self.localMem += memory
        self.ssd += ssd
        self.updateMCE()

    def finishTask(self, taskId):
        self.localMem = self.localMem + self.runningTasks[taskId].localMem
        self.ssd = self.ssd + self.runningTasks[taskId].ssd
        del self.server_runningTasks[taskId]
        self.updateMCE()

    def finishFarTask(self, farMem):
        self.localMem = self.localMem + farMem

    # def getMaxMCEtask(self):
    #     maxMCE = -float('inf')
    #     maxMCEtask = self.runningTasks[0]
    #     for t in self.runningTasks:
    #         if t.mce > maxMCE:
    #             maxMCEtask = t
    #             maxMCE = t.mce
    #     return maxMCEtask

    #TODO  
    def updateMCE(self):
        self.mce = self.localMem
        for task in self.server_runningTasks:
            tmce = task.mce
            self.task_mce_list.append(tmce)
            self.mce =self.mce + tmce
        # if (len(self.server_runningTasks)== 0):
        #     average = 0
        # else:
        #     average = self.mce / len(self.server_runningTasks)
        # self.alias_task_mce_list = [(m-average) for m in self.task_mce_list]
        # self.least_mce_task = min(self.task_mce_list)
        # print('sever '+repr(self.id)+' updated mce is '+repr(self.mce))
