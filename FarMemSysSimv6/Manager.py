import numpy as np
import pandas as pd
import random
import copy

from Cluster import Cluster
from Server import Server,MAX_SSD,MAX_MEMORY
from Task import Task

tasknum = 2000
ServerNum = 50

profiles = { }
index    = [0, 1,   2,   3,   4,   5,   6,   7,   8,   9,  10]
non_sens = [1, 1, 1.1, 1.1, 1.1, 1.1, 1.2, 1.2, 1.2, 1.3, 1.3]
#part_non = [1, 1, 1.1, 1.1, 1.1, 1.2, 1.2, 1.5, 2.3, 3.5, 5.0]
ave_sens = [1, 2, 2.3, 2.7, 3.7, 4.9,   6, 7.2, 8.9, 9.7, 10.8]
full_sens= [1, 3, 6.2, 6.8, 7.2, 7.6, 7.9,   8, 8.1, 8.2, 8.3 ]

part_non = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

def creatCluster():
    serverNum = ServerNum #default: 50
    serverMem = MAX_MEMORY  #default: 20000, memory size of every server(unit?)
    serverSSD = MAX_SSD  #default: 2000000, ssd capacity of every server(unit?)
    serverList = []
    for i in range(serverNum):
        server = Server(i, serverMem, serverSSD)
        serverList.append(server)
    return Cluster(serverList)

#TODO
def taskGenerator(tasknum):
    taskList = []
    for i in range(tasknum):
        base_runtime = 10
        base_pagefault = 100
        latency_list = [i * base_runtime for i in part_non]
        pagefaultlist =[j * base_pagefault for j in part_non]
        #task = Task(i, 1000 + random.randint(0,1000),latency_list,pagefaultlist,random.randint(1,9)) # def __init__(self, memory, latencylist, pagefaultlist, leastlocalratio:int):
        task = Task(i, 1000 + random.randint(0, 1000), latency_list, pagefaultlist, (1 + random.randint(1, 10) * 0.1))
        print("task " + repr(task.id) + '： least local ratio = ' + repr(task.leastlocalratio) + ' task memory = ' +repr(task.memory) +' task SLA latency = ' +repr(task.longestLatancy))
        taskList.append(task)
    return taskList


def realTaskGenerator():
    taskList = []
    global_SLA = 1.5 #TODO: 什么是global_SLA
    # 模拟一个task需要基础的task_id， 占用内存，它的latency_list和pagefault_list，还有一个global_SLA
    quicksort2G = Task(0,2052,
                       [74.3,104.81,111.44,129.44,143.35,156.21,172.57,188.5,999999999,999999999,999999999],
                       [2,3033474,314198,449932,488308,671468,665971,971614,999999999,999999999,999999999],
                       global_SLA)
    quicksort2G.type = 0 #TODO: 这个type是什么
    print("quicksort2G: task " + repr(quicksort2G.id) + '： least local ratio = ' + repr(quicksort2G.leastlocalratio) + ' task memory = ' +repr(quicksort2G.memory) +' task SLA latency = ' +repr(quicksort2G.longestLatancy))
    taskList.append(quicksort2G)

    quicksort8G = Task(1, 8113,
                       [302.53, 379.46, 491.77, 490.68, 571.31, 594.4, 652.43, 999999999, 999999999, 999999999, 999999999],
                       [0, 389205,1050773, 1041501,1283474,1686028,2854462, 999999999, 999999999, 999999999, 999999999],
                       global_SLA)
    quicksort8G.type = 1
    print("quicksort8G: task " + repr(quicksort8G.id) + '： least local ratio = ' + repr(
        quicksort8G.leastlocalratio) + ' task memory = ' + repr(quicksort8G.memory) + ' task SLA latency = ' + repr(
        quicksort8G.longestLatancy))
    taskList.append(quicksort8G)

    fsImage1G = Task(2, 1366,
                       [1039.28,1066.66,1084.33,1106.05,1115.14,1125.34,1134.17,1110.65, 1120, 1900, 999999999],
                       [2029,2102,2219,3893,15850,31555,53105,109670, 199670, 339670, 999999999],
                       global_SLA)
    fsImage1G.type = 2
    print("fsImage1G: task " + repr(fsImage1G.id) + '： least local ratio = ' + repr(
        fsImage1G.leastlocalratio) + ' task memory = ' + repr(fsImage1G.memory) + ' task SLA latency = ' + repr(
        fsImage1G.longestLatancy))

    taskList.append(fsImage1G)

    fsVideo26G = Task(3, 1765,
                       [26999.76,25552.46,28986,29409.2,29638.39,29812.98,36539.01,37973.48, 999999999, 999999999, 999999999],
                       [2145,2202,2710,12338,87972,830075,1725776,2280794, 999999999, 999999999, 999999999],
                       global_SLA)
    fsVideo26G.type = 3
    print("fsVideo26G: task " + repr(fsVideo26G.id) + '： least local ratio = ' + repr(
        fsVideo26G.leastlocalratio) + ' task memory = ' + repr(fsVideo26G.memory) + ' task SLA latency = ' + repr(
        fsVideo26G.longestLatancy))
    taskList.append(fsVideo26G)

    fsVideo = Task(4, 1970,
                      [1393.55,1052.24,1571.79,1243.04,2037.98,5273.67,9312.48,6423.38, 999999999, 999999999, 999999999],
                      [2153,2187,3354,9902,59650,835926,1638375,1928275, 999999999, 999999999, 999999999],
                      global_SLA)
    fsVideo.type = 4
    print("fsVideo: task " + repr(fsVideo.id) + '： least local ratio = ' + repr(
        fsVideo.leastlocalratio) + ' task memory = ' + repr(fsVideo.memory) + ' task SLA latency = ' + repr(
        fsVideo.longestLatancy))
    taskList.append(fsVideo)

    ligraBfs5G = Task(5, 4548,
                   [15.77,14.76,17.69,28.51,31.96,39.44,46.38,53.24, 999999999, 999999999, 999999999],
                   [4,3,3,23790,74456,176406,228077,214191, 999999999, 999999999, 999999999],
                   global_SLA)
    ligraBfs5G.type = 5
    print("ligraBfs5G: task " + repr(ligraBfs5G.id) + '： least local ratio = ' + repr(
        ligraBfs5G.leastlocalratio) + ' task memory = ' + repr(ligraBfs5G.memory) + ' task SLA latency = ' + repr(
        ligraBfs5G.longestLatancy))
    taskList.append(ligraBfs5G)

    ligraBfs19G = Task(6, 19011,
                      [67.24,59.29,67.31,92.77,118.37,110.69,113.55,163.72, 999999999, 999999999, 999999999],
                      [4,3,4,208521,327845,226452,224577,555622, 999999999, 999999999, 999999999],
                      global_SLA)
    ligraBfs19G.type = 6
    print("ligraBfs19G: task " + repr(ligraBfs19G.id) + '： least local ratio = ' + repr(
        ligraBfs19G.leastlocalratio) + ' task memory = ' + repr(ligraBfs19G.memory) + ' task SLA latency = ' + repr(
        ligraBfs19G.longestLatancy))
    taskList.append(ligraBfs19G)

    ligraPr5G = Task(7, 4548,
                       [37.86,35.98,38.01,45.22,54.14,48.95,50.65,80.73, 999999999, 999999999, 999999999],
                       [4,3,4,48457,90276,72765,60547,231216, 999999999, 999999999, 999999999],
                       global_SLA)
    ligraPr5G.type = 7
    print("ligraPr5G: task " + repr(ligraPr5G.id) + '： least local ratio = ' + repr(
        ligraPr5G.leastlocalratio) + ' task memory = ' + repr(ligraPr5G.memory) + ' task SLA latency = ' + repr(
        ligraPr5G.longestLatancy))
    taskList.append(ligraPr5G)

    ligraPr19G = Task(8, 19010,
                     [171.3,184.06,181.92,209.15,226.97,218.68,260.61,290.7, 999999999, 999999999, 999999999],
                     [4,4,4,181630,247854,226006,579776,578512, 999999999, 999999999, 999999999],
                     global_SLA)
    ligraPr19G.type = 8
    print("ligraPr19G: task " + repr(ligraPr19G.id) + '： least local ratio = ' + repr(
        ligraPr19G.leastlocalratio) + ' task memory = ' + repr(ligraPr19G.memory) + ' task SLA latency = ' + repr(
        ligraPr19G.longestLatancy))
    taskList.append(ligraPr19G)

    ffmpegMkv6G = Task(9, 2513,
                      [6144.11,6083.49,6057,6072.95,6162.78,5956.54,6076.8,6113.75, 6413.75, 999999999, 999999999],
                      [139,137,133,137,138,128,145,128, 245, 999999999, 999999999],
                      global_SLA)
    ffmpegMkv6G.type = 9
    print("ffmpegMkv6G: task " + repr(ffmpegMkv6G.id) + '： least local ratio = ' + repr(
        ffmpegMkv6G.leastlocalratio) + ' task memory = ' + repr(ffmpegMkv6G.memory) + ' task SLA latency = ' + repr(
        ffmpegMkv6G.longestLatancy))
    taskList.append(ffmpegMkv6G)

    ffmpegMp48G = Task(10, 3291,
                       [8393.65,8402.4,8426.11,8385.44,8417.87,8396.66,8359.86,8451.08, 8551.08, 999999999, 999999999],
                       [67,71,86,84,72,84,83,87, 96, 999999999, 999999999],
                       global_SLA)
    ffmpegMp48G.type = 10
    print("ffmpegMp48G: task " + repr(ffmpegMp48G.id) + '： least local ratio = ' + repr(
        ffmpegMp48G.leastlocalratio) + ' task memory = ' + repr(ffmpegMp48G.memory) + ' task SLA latency = ' + repr(
        ffmpegMp48G.longestLatancy))
    taskList.append(ffmpegMp48G)

    tfInception4G = Task(11, 3267,
                       [215.71,219.16,221.25,225.41,238.22,254.62,257.22,266.04, 270.04, 999999999, 999999999],
                       [2952,3400,19609,30946,47780,86056,95059,135677, 165677, 999999999, 999999999],
                       global_SLA)
    tfInception4G.type = 11
    print("tfInception4G: task " + repr(tfInception4G.id) + '： least local ratio = ' + repr(
        tfInception4G.leastlocalratio) + ' task memory = ' + repr(tfInception4G.memory) + ' task SLA latency = ' + repr(
        tfInception4G.longestLatancy))
    taskList.append(tfInception4G)

    tfResnet4G = Task(12, 3196,
                         [166.64,164.64,170.96,174.5,172.02,180.21,183.66,193.3, 200.3, 999999999, 999999999],
                         [2953,3199,19041,20489,28145,42911,44831,72728, 100028, 999999999, 999999999],
                         global_SLA)
    tfResnet4G.type = 12
    print("tfResnet4G: task " + repr(tfResnet4G.id) + '： least local ratio = ' + repr(
        tfResnet4G.leastlocalratio) + ' task memory = ' + repr(tfResnet4G.memory) + ' task SLA latency = ' + repr(
        tfResnet4G.longestLatancy))
    taskList.append(tfResnet4G)

    return taskList



def realTaskGeneratorN(tasknum):
    """
    There are several typical task, we use random algorithm to chose task then put into our result list
    """
    realTaskList = realTaskGenerator()
    taskList = []
    i = 0
    while i in range(tasknum):
    # for i in range(tasknum):
        task = copy.deepcopy(random.choice(realTaskList))# random.choise随机选择一个task
        task.updateID(i)
        print(
            "task " + repr(task.id) + '： least local ratio = ' + repr(task.leastlocalratio) + ' task memory = ' + repr(
                task.memory) + ' task SLA latency = ' + repr(task.longestLatancy) + ' task type = ' + repr(task.type))
        taskList.append(task)
        i=i+1
    return taskList



def full_match(task, cluster):
    """
    按顺序找到合适的server后assign这个task给这个server。

    :param task: The task to assign
    :param cluster: The cluster to hold the task
    :return: [(true if the task has been assigned),(The id of server that hold the task, -100 mean no server memory match), ()]
    """
    #print('full_match start')
    allocMem = 0
    # tmce = task.mce
    # alias_smceList = cluster.alias_mcelist
    for s in cluster.servers:
        if task.memory <= s.localMem:
            allocMem = task.memory
            #matched_server =s
            print('full match : ' + 'Server ' + repr(s.id) + ' has '+ repr(s.localMem) + ' memory to hold task '+repr(task.id))
            #update server
            task.localMem = allocMem
            task.localServer = s
            task.updateMCE()
            s.addTask(task, allocMem)
            print('sever ' + repr(s.id) +' add task '+repr(task.id)+', server.memory is '  + repr(s.localMem)+ ' sever mce = ' + repr(s.mce))
            print('sever id = ' + repr(s.id) + ' has '+str(len(s.server_runningTasks))+' tasks, sever mce = ' + repr(s.mce))
            print ()
            return True, s.id, allocMem
    return False ,-100, allocMem

def worst_press_server(task, cluster):
    print ()
    allocMem = 0
    for s in cluster.servers:
        # 新分配的任务也是SLA
        # print('sever id = ' +repr(s.id)+ ' sever mce = ' +repr(s.mce))
        if s.localMem >= task.leastlocalmemory:
            allocMem = task.leastlocalmemory
            matched_server = s
            task.localMem = allocMem
            task.updateMCE()
            task.localServer = matched_server
            matched_server.addTask(task, allocMem)
            # matched_server.updateMCE()
            print( "add  task " + repr(task.id) + ' to Server ' + repr(s.id) + ' server rest memory is ' + repr(s.localMem))
            return True, matched_server.id, allocMem
        elif s.mce >= task.leastlocalmemory:
            # 把每一个现有task都压缩为SLA，更新server memory
            print('press sever '+str(s.id)+' current tasks to leastlocalmemory')
            for t in s.server_runningTasks:
                #t = s.runningTasks[tid]
                t.localMem = t.leastlocalmemory
                t.updateMCE()
                s.localMem = s.localMem +(t.memory -t.localMem)
            allocMem = task.leastlocalmemory
            matched_server = s
            task.localMem = allocMem
            task.localServer = matched_server
            task.updateMCE()
            matched_server.addTask( task, allocMem)
            # matched_server.updateMCE()
            # print('Server ' + repr(s.id) + " can hold the task " + repr(task.id) + " if squeezing current tasks to SLA")
            print("add  task " + repr(task.id) + ' to Server ' + repr(s.id) + ' server rest memory is ' + repr(s.localMem))
            return True, matched_server.id, allocMem
        else:
            continue
    print('match failed')
    return False, s.id, allocMem


def press_server(task, cluster):
    print('press_server start')
    allocMem = 0
    for s in cluster.servers:
        if s.localMem <= 1:  ##1M reserved
            print('Server ' + repr(s.id) + " has no memory to hold task " + repr(task.id) + ', try next server')
            continue
        if allocMem == 0:
            # print('Server ' + repr(s.id) + " cannot hold the full task" + repr(task.id))
            if s.localMem >= task.leastlocalmemory:
                allocMem = s.localMem
                matched_server = s
                task.localMem = allocMem
                task.localServer = matched_server
                matched_server.addTask( task, allocMem)
                matched_server.updateMCE()
                print('Server ' + repr(s.id) + " can hold the task " + repr(task.id) + "with least local memory")
                return True, matched_server.id, allocMem
    for s in cluster.servers:
        if s.mce >= task.leastlocalmemory:
            allocMem = task.leastlocalmemory
            matched_server = s
            task.localMem = allocMem
            print('Server ' + repr(s.id) + " can hold the task " + repr(task.id) + "if squeezing current tasks to SLA")
            return True, matched_server.id, allocMem
        else:
            continue
    print('match failed')
    return False, s.id, allocMem

    # matched_server.localMem = matched_server.localMem - task.memory

# find_far(task, task.localserver, cluster)
def find_far(task, serverId, cluster):
    print("find far server for task" +repr(task.id))
    for s in cluster.servers:
        if s.localMem <= 2:
            continue
        if s.id == serverId:
            continue
        if task.hfm <= (0-s.mce):
            farTask = s.least_mce_task
            task.farServer = s
            return s.id, task.hfm, farTask, True
        else: continue
    return task.localServer, 0,task, False

def fit(task, serverid, cluster):
    ifsuccess, ltask, fartask, server =  inner_fit_one_task(task, serverid, cluster)
    return ifsuccess, ltask, fartask, server

def inner_fit_one_task(task, serverid, cluster):
    print("inner_fit start")
    server = cluster.servers[serverid]
    fartask = server.least_mce_task
    server.addTask(task, task.localMem)
    server.updateMCE()

    while (server.alias_task_mce_list[task.id] > 0 & server.alias_task_mce_list[fartask.id] < 0):
        server.resetTask(task.id, task, task.localMem+100, task.localMem-100)
        server.resetTask(fartask.id, fartask, fartask.localMem-100, fartask.localMem + 100)
        server.updateMCE()
        task.updateMCE()
    print("inner_fit finished. task.local memory = " +repr(task.localMem) )
    return True, task, fartask, server

def inter_fit(task, localserverid, farserverid, cluster):
    print("inter_fit start")
    localserver = cluster.servers[localserverid]
    farserver = cluster.servers[farserverid]
    #update task hfm
    localserver.addTask(task, task.localMem)
    farserver.addTask( task, task.hfm)
    while (cluster.alias_mcelist[localserver.id] >0 & cluster.alias_mcelist[farserver.id] <0):
        task.hfm = task.hfm + 100
        task.updateMCE()
        localserver.resetTask(task.id, task, task.localMem, task.ssd)
        farserver.resetTask(task.id, task, task.hfm, 0)
        localserver.updateMCE()
        farserver.updateMCe()
    #allocate hfm
    cluster.allocFarTask(task, task.hfm, localserver, farserver)
    return True, task.id, task.hfm, localserver.id, farserver.id

def sort_by_mce(taskList):
     #todo
  #   for task in taskList:
  #       idlist.append(task.id)
     #sorted_tasklist = idlist.sort(key=task.id, reverse=False)
     taskList.sort(key = lambda x: x.fixed_mce)
     #for i in taskList:
     #    print (i.mce)
     #print('task list sort')
     return taskList

def worst_allocateTasks(taskList, cluster):
    # 先给taskList里的task根据mce排序。
    sorted_taskList = sort_by_mce(taskList)
    for task in sorted_taskList:
        print("task " + repr(task.id) + '： fixed_mce =  ' + repr(task.fixed_mce))
        # assign all task to the cluster.

    for task in sorted_taskList:
        # TODO: full match 貌似是直接随便分配的意思。
        ifmatchsuccess, localServerId, localMem = full_match(task, cluster)
    for task in sorted_taskList:
        if task.localMem == 0: #& ifmatchsuccess == False:
            # cluster.servers[localServerId].addTask( task, localMem)
            # TODO: 这个worst press到底在干什么
            ifsuccess, sid, alm = worst_press_server(task, cluster)
            if ifsuccess == False:
                print("wait")

    # 所有task分配完毕，打印汇总信息。
    for sever in cluster.servers:
        print ()
        print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; mce:'+str(sever.mce))
        for task in sever.server_runningTasks:
            print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; mce:'+str(task.mce)+'; hfm:'+str(task.hfm))


def oracle_allocateTasks(taskList, cluster):
    # 先给taskList里的task根据mce排序。
    sorted_taskList = sort_by_mce(taskList)
    for task in sorted_taskList:
        print("task " + repr(task.id) + '： fixed_mce =  ' + repr(task.fixed_mce))

    for task in sorted_taskList:
        # 每一次，都要根据cluster里server的mce值进行重新排序排序。
        cluster.servers.sort(key=lambda x: x.mce,reverse = True)
        # 排序后，按顺序找到最匹配的server，把这个task assign进去。
        for sever in cluster.servers:
            if sever.localMem > task.leastlocalmemory:
                allocMem = task.leastlocalmemory
                matched_server = sever
                task.localMem = allocMem
                task.localServer = matched_server
                task.updateMCE()
                matched_server.addTask(task, allocMem)
                # matched_server.updateMCE()
                print("add  task " + repr(task.id) + ' to Server ' + repr(sever.id) + ' server rest memory is ' + repr(sever.localMem))
                break
            else:
                # 没找到合适的server，下一个。
                continue
    # 分配完所有task后，打印最终结果信息。
    for sever in cluster.servers:
        print ()
        print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; mce:'+str(sever.mce))
        for task in sever.server_runningTasks:
            print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; mce:'+str(task.mce)+'; hfm:'+str(task.hfm))



# def worst_match(cluster):
#     print ()
#     for s in cluster.servers:
#         if s.mce == s.localMem:
#             transfer_Mem = s.localMem / len(s.server_runningTasks)
#             for task in s.server_runningTasks:
#                 task.localMem = task.localMem + transfer_Mem
#                 s.localMem = s.localMem - transfer_Mem
#                 task.updateMCE()
#             s.updateMCE()
#     for sever in cluster.servers:
#         print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; mce:'+str(sever.mce))
#         for task in sever.server_runningTasks:
#             print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; mce:'+str(task.mce)+'; hfm:'+str(task.hfm))
#         print ()


def worst_match(cluster):
    print ()
    for s in cluster.servers:
        if s.mce == s.localMem:
            needMem = 0
            for task in s.server_runningTasks:
                needMem = needMem + task.memory - task.localMem
            if needMem > s.localMem:  # localmem可以都分出去，不会出现task已经fullmem了
                transfer_Mem = s.localMem / len(s.server_runningTasks)
            else:
                transfer_Mem = needMem / len(s.server_runningTasks)
            for task in s.server_runningTasks:
                task.localMem = task.localMem + transfer_Mem
                s.localMem = s.localMem - transfer_Mem
                task.updateMCE()
            s.updateMCE()
    for sever in cluster.servers:
        print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; mce:'+str(sever.mce))
        for task in sever.server_runningTasks:
            print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; mce:'+str(task.mce))
        print ()

def oracle_match(cluster):
    print ()
    for s in cluster.servers:
        needMem = 0
        for task in s.server_runningTasks:
            needMem = needMem+task.memory-task.localMem

        if needMem>s.localMem: #localmem可以都分出去，不会出现task已经fullmem了
            transfer_Mem = s.localMem / len(s.server_runningTasks)
        else:
            transfer_Mem = needMem / len(s.server_runningTasks)
        for task in s.server_runningTasks:
            task.localMem = task.localMem+transfer_Mem
            s.localMem = s.localMem - transfer_Mem
            task.updateMCE()
        s.updateMCE()

    for sever in cluster.servers:
        print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; mce:'+str(sever.mce))
        for task in sever.server_runningTasks:
            print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; mce:'+str(task.mce) +'; hfm:'+str(task.hfm))
        print ()

def ratio_according2fixedmce(tasks):
    pai_fixed_mce = 1
    ratio = []
    for task in tasks:
        pai_fixed_mce = pai_fixed_mce * task.fixed_mce
    for task in tasks:
        ratio.append(pai_fixed_mce / task.fixed_mce)
    sum = np.sum(ratio)
    ratio = ratio / sum
    return ratio

# def worst_inner(cluster):
#     print ()
#     for s in cluster.servers:
#         if s.mce == s.localMem:
#             transfer_Mem = s.localMem
#             ratio = ratio_according2fixedmce(s.server_runningTasks)
#             i = 0
#             for task in s.server_runningTasks:
#                 task.localMem = task.localMem+ transfer_Mem*ratio[i]
#                 s.localMem = s.localMem - transfer_Mem*ratio[i]
#                 task.updateMCE()
#                 i = i+1
#             s.updateMCE()
#     for sever in cluster.servers:
#         print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; mce:'+str(sever.mce))
#         for task in sever.server_runningTasks:
#             print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; mce:'+str(task.mce) +'; hfm:'+str(task.hfm))
#         print ()

def worst_inner(cluster):
    print ()
    for s in cluster.servers:
        if s.mce == s.localMem:
            needMem = 0
            for task in s.server_runningTasks:
                needMem = needMem + task.memory - task.localMem #把localMem减去，这是只剩remoteMem
            if needMem > s.localMem:  # localmem可以都分出去，不会出现task已经fullmem了
                #ccy:needMem如果是remoteMem的话，大于s.localMeme
                transfer_Mem = s.localMem / len(s.server_runningTasks)
            else:
                transfer_Mem = needMem / len(s.server_runningTasks)
            # transfer_Mem = s.localMem
            ratio = ratio_according2fixedmce(s.server_runningTasks)
            i = 0
            for task in s.server_runningTasks:
                task.localMem = task.localMem+ transfer_Mem*ratio[i]
                s.localMem = s.localMem - transfer_Mem*ratio[i]
                task.updateMCE()
                i = i+1
            s.updateMCE()
    for sever in cluster.servers:
        print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; mce:'+str(sever.mce))
        for task in sever.server_runningTasks:
            print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; mce:'+str(task.mce))
        print ()


def oracle_inner(cluster):
    print ()
    for s in cluster.servers:
        needMem = 0
        for task in s.server_runningTasks:
            needMem = needMem + task.memory - task.localMem
        if needMem > s.localMem:# localmem可以都分出去，不会出现task已经fullmem了
            transfer_Mem = s.localMem
        else:# localmem不可以都分出去，会出现task已经fullmem了
            transfer_Mem = needMem
        ratio = ratio_according2fixedmce(s.server_runningTasks)
        i = 0
        for task in s.server_runningTasks:
            task.localMem = task.localMem+ transfer_Mem*ratio[i]
            s.localMem = s.localMem - transfer_Mem*ratio[i]
            task.updateMCE()
            i = i+1
        s.updateMCE()


    for sever in cluster.servers:
        print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; mce:'+str(sever.mce))
        for task in sever.server_runningTasks:
            print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; mce:'+str(task.mce) )
        print ()

def worst_inter(worst_inner_cluster):
    print ()
    sum_mce = 0
    for s in worst_inner_cluster.servers:
        sum_mce = sum_mce+s.mce
    ave_mce = sum_mce/len(worst_inner_cluster.servers)
    for s in worst_inner_cluster.servers:
        if s.mce<ave_mce:# 转入mem
            s.farMem = ave_mce-s.mce # 正值
            transfer_Mem = s.farMem
            i = 0
            ratio = ratio_according2fixedmce(s.server_runningTasks)
            for task in s.server_runningTasks:
                task.farMem = task.farMem + transfer_Mem * ratio[i]
                i = i+1
                task.updateMCE()
            s.updateMCE()
        else: # 转出mem
            s.farMem = ave_mce - s.mce # 负值
            if s.localMem > -1*s.farMem: # 空闲的mem就够了
                s.localMem = s.localMem + s.farMem
            else: # 空闲的mem不够了
                s.localMem = 0
                transfer_FarMem = s.farMem +s.localMem
                all_mce = 0
                for task in s.server_runningTasks:
                    all_mce = all_mce + task.mce
                for task in s.server_runningTasks:
                    task.farMem = transfer_FarMem * task.mce / all_mce
                    task.localMem = task.localMem + task.farMem
                    task.updateMCE()
            s.updateMCE()

    for sever in worst_inner_cluster.servers:
        print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; farMem:'+str(sever.farMem)+'; mce:'+str(sever.mce))
        for task in sever.server_runningTasks:
            print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; farMem:'+str(task.farMem)+'; mce:'+str(task.mce)+'; est_latency:'+str(task.estimate_latency_by_profile()))
        print ()


def oracle_inter(oracle_inner_cluster):
    print ()
    sum_mce = 0
    for s in oracle_inner_cluster.servers:
        sum_mce = sum_mce+s.mce
    ave_mce = sum_mce/len(oracle_inner_cluster.servers)
    for s in oracle_inner_cluster.servers:
        if s.mce<ave_mce:# 转入mem
            s.farMem = ave_mce-s.mce # 正值
            transfer_Mem = s.farMem
            i = 0
            ratio = ratio_according2fixedmce(s.server_runningTasks)
            for task in s.server_runningTasks:
                task.farMem = task.farMem + transfer_Mem * ratio[i]
                i = i+1
                task.updateMCE()
            s.updateMCE()
        else: # 转出mem
            s.farMem = ave_mce - s.mce # 负值
            if s.localMem > -1*s.farMem: # 空闲的mem就够了
                s.localMem = s.localMem + s.farMem
            else: # 空闲的mem不够了
                s.localMem = 0
                transfer_FarMem = s.farMem +s.localMem
                all_mce = 0
                for task in s.server_runningTasks:
                    all_mce = all_mce + task.mce
                for task in s.server_runningTasks:
                    task.farMem = transfer_FarMem * task.mce / all_mce
                    task.localMem = task.localMem + task.farMem
                    task.updateMCE()
            s.updateMCE()

    for sever in oracle_inner_cluster.servers:
        print ('Sever id: '+ str(sever.id)+'; localMem:'+str(sever.localMem)+'; farMem:'+str(sever.farMem)+'; mce:'+str(sever.mce))
        for task in sever.server_runningTasks:
            print ('Task id: '+ str(task.id)+'; memory:'+str(task.memory)+'; localMem:'+str(task.localMem)+'; farMem:'+str(task.farMem)+'; mce:'+str(task.mce) +'; est_latency:'+str(task.estimate_latency_by_profile()))
        print ()


# def allocateTasks(taskList, cluster):
#     sorted_taskList = sort_by_mce(taskList) #
#     for task in sorted_taskList:
#         ifmatchsuccess, localServerId, localMem = full_match(task, cluster)
#         if ifmatchsuccess == False:
#            # cluster.servers[localServerId].addTask( task, localMem)
#             ifsuccess, sid, alm = match(task, cluster)
#             print("try to full_match -> match" )
#             if ifsuccess == False:
#                 print("wait")

        # if localMem < task.memory:
        #     farServerId, farMem, farTask, iffitSuccess = find_far(task, localServerId, cluster)
        #     while not iffitSuccess:
        #         if cluster.finishTask():
        #             farServerId, farMem, farTask, ifSuccess = find_far(task, localServerId, cluster)
        #             print("Fit success")
        #         else:
        #             print("No Running Task")
        #     ssd = task.memory - localMem - farMem
        #     task.setRunInfo(localServerId, localMem, farServerId, farMem, ssd, cluster.nowTime)
        #     cluster.allocWithFarTask(task, farTask)
        # else:
        #     ssd = task.memory - localMem
        #     task.setRunInfo(localServerId, localMem, 0, 0.0, ssd, cluster.nowTime)
        #     # for s in cluster.servers:
        #     #     if s.id == localServerId:
        #     #         farTask = s.getMaxMCEtask()
        #     cluster.allocTask(task)
def output_tasks(cluster, filestring):
    server_id = 0
    task_id = [0]
    task_server = [0]
    task_latency = [0.0]
    task_localmemory = [0.0]
    task_leastlocalratio = [0]
    task_shortestLatancy = [0.0]
    task_fullmemory = [0.0]
    task_farmemory = [0.0]
    result = []
    server_result = []
    for server in cluster.servers:
        #server_mce.append(server.mce)
        for task in server.server_runningTasks:
            task_id.append(task.id)
            task_server.append(task.localServer)
            task_leastlocalratio.append(task.leastlocalratio)
            task_shortestLatancy.append(task.shortestLatancy)
            task_latency.append(task.estimate_latency_by_profile())
            task_fullmemory.append(task.memory)
            task_localmemory.append(task.localMem)

    result.append(task_id)
    result.append(task_server)
    result.append(task_leastlocalratio)
    result.append(task_shortestLatancy)
    result.append(task_latency)
    result.append(task_fullmemory)
    result.append(task_localmemory)
    array = np.array(result)
    df = pd.DataFrame(array)
    print(result)
    df.to_csv(filestring)
    result.clear()
    #     print(result)
    #     server_result.append(copy.deepcopy(result))
    #     server_id = server_id +1
    #     task_id.clear()
    #     task_latency.clear()
    #     task_localmemory.clear()
    #     task_farmemory.clear()
    #     result.clear()
    # array = []
    # i=0
    #print(server_result)

    # for serveri in server_result:
    #     array = np.array(serveri)
    #     df = pd.DataFrame(array)
    #     df.to_csv('output/server_result'+str(i) +'.csv')
    #     i=i+1





if __name__ == '__main__':
    cluster = creatCluster()
    # waitingTasks = taskGenerator(tasknum)
    #waitingTasks = realTaskGenerator()
    waitingTasks = realTaskGeneratorN(tasknum) #default tasknum is 2000

    print ('--------------------------------- worst allocate Start-----------------------------------------------')
    worst_allocate_cluster = copy.deepcopy(cluster)
    worst_allocateTasks(waitingTasks, worst_allocate_cluster)

    print ('--------------------------------- Worst Match Start-----------------------------------------------')
    worst_match_cluster = copy.deepcopy(worst_allocate_cluster)
    worst_match(worst_match_cluster)

    print ('--------------------------------- Worst Inner Start-----------------------------------------------')
    worst_inner_cluster = copy.deepcopy(worst_allocate_cluster)
    worst_inner(worst_inner_cluster)

    print ('--------------------------------- Worst Inter Start-----------------------------------------------')
    worst_inter_cluster = copy.deepcopy(worst_inner_cluster)
    worst_inter(worst_inter_cluster)
    # output_tasks(worst_inter_cluster, 'output/task_result_worst_inter_' + str(tasknum) + '.csv')

    print ('--------------------------------- Oracle allocate Start-----------------------------------------------')
    oracle_allocate_cluster = copy.deepcopy(cluster)
    # 这把task按最好的方式分配给cluster里的各个server
    oracle_allocateTasks(waitingTasks, oracle_allocate_cluster)

    print ('--------------------------------- Oracle Match Start-----------------------------------------------')
    oracle_match_cluster = copy.deepcopy(oracle_allocate_cluster)
    oracle_match(oracle_match_cluster)

    print ('--------------------------------- Oracle Inner Start-----------------------------------------------')
    oracle_inner_cluster = copy.deepcopy(oracle_allocate_cluster)
    oracle_inner(oracle_inner_cluster)

    print ('--------------------------------- Oracle Inter Start-----------------------------------------------')
    oracle_inter_cluster = copy.deepcopy(oracle_inner_cluster)
    oracle_inter(oracle_inter_cluster)

    # output_tasks(oracle_inter_cluster,'output/task_result_oracle_inter_' +str(tasknum) + '.csv')
    print("end")
    #allocateTasks(waitingTasks, cluster)
    # while cluster.finishTask():
    #     True
    # sumTime = cluster.nowTime
    # print("end")
    # print(sumTime)





