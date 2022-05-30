from curses import meta
import subprocess
import os
import numpy as np
import struct
import pandas as pd

# LOAD_LIST = '/home/wjing/hfm-workloads'
app_list = [
    

    # # tensorflow
    # '/usr/bin/time -v /home/wjing/hfm-workloads/tensorflow/tf-inception.sh', 
    # '/usr/bin/time -v /home/wjing/hfm-workloads/tensorflow/tf-resnet.sh',

    # #fsdet
    # 'cd /home/wjing/hfm-workloads/few-shot-object-detection && /usr/bin/time -v /home/meijunyi/anaconda3/envs/farmem/bin/python -m demo.demo --config-file configs/COCO-detection/faster_rcnn_R_101_FPN_ft_all_1shot.yaml   --input ../input/bike.jpg --output output/ --opts MODEL.WEIGHTS fsdet://coco/tfa_cos_1shot/model_final.pth  MODEL.DEVICE cpu',
    # 'cd /home/wjing/hfm-workloads/few-shot-object-detection && /usr/bin/time -v /home/meijunyi/anaconda3/envs/farmem/bin/python -m demo.demo --config-file configs/COCO-detection/faster_rcnn_R_101_FPN_ft_all_1shot.yaml   --video-input ../input/test2.mp4 --output output/ --opts MODEL.WEIGHTS fsdet://coco/tfa_cos_1shot/model_final.pth  MODEL.DEVICE cpu',

    

    # #ffmpeg 
    'rm /home/wjing/hfm-workloads/output/out* &&/usr/bin/time -v /home/wjing/hfm-workloads/ffmpeg-4.4.1/ffmpeg -i /home/wjing/hfm-workloads/input/duye.mkv /home/wjing/hfm-workloads/output/out-duye.mkv', 
    # 'rm /home/wjing/hfm-workloads/output/out* &&/usr/bin/time -v /home/wjing/hfm-workloads/ffmpeg-4.4.1/ffmpeg -i /home/wjing/hfm-workloads/input/avengers.mkv /home/wjing/hfm-workloads/output/out-avengers.mkv', 

    

    #ligra
    # '/usr/bin/time -v /home/wjing/ligra/apps/BFS -s -r 1 /home/wjing/ligra/inputs/rMat_10000000', 
    # '/usr/bin/time -v /home/wjing/ligra/apps/BFS -s -r 1 /home/wjing/ligra/inputs/rMat_40000000',
    # '/usr/bin/time -v /home/wjing/ligra/apps/PageRank -s -r 1 /home/wjing/ligra/inputs/rMat_10000000',
    # '/usr/bin/time -v /home/wjing/ligra/apps/PageRank -s -r 1 /home/wjing/ligra/inputs/rMat_40000000',

    #quicksort
    # '/usr/bin/time -v /home/wjing/hfm-workloads/quicksort/quicksort 2047', 
    # '/usr/bin/time -v /home/wjing/hfm-workloads/quicksort/quicksort 8096',

]

def get_cmd(app_index,metabytes):
    '''
    获取shell命令
    '''

    clear = 'sudo sh -c "echo 3 > /proc/sys/vm/drop_caches"'
    # swappiness = 'sudo sh -c "sysctl vm.swappiness=0"'
    rmdir = 'sudo rmdir /sys/fs/cgroup/memory/farmemory'
    mkdir = 'sudo mkdir /sys/fs/cgroup/memory/farmemory'
    limit = ''
    if metabytes ==-1:
        limit = 'sudo sh -c "echo -1 > /sys/fs/cgroup/memory/farmemory/memory.limit_in_bytes"'
    else:
        limit = 'sudo sh -c "echo {}M > /sys/fs/cgroup/memory/farmemory/memory.limit_in_bytes"'.format(metabytes)
    procs = 'sudo sh -c "echo $$  > /sys/fs/cgroup/memory/farmemory/cgroup.procs"'
    # exe  = '/usr/bin/time -v {}'.format(app_list[app_index])
    exe = app_list[app_index]
    full_cmd = " && ".join((clear,rmdir,mkdir,limit,procs,exe))
    return full_cmd

def get_data(res):
    '''
    获取运行时间和算法时间，缺页中断的次数
    '''
    cpu_time = 0.0 #程序占据cpu的运行时间
    system_time = 0.0
    page_fault = 0
    for line in res:
        # print(line)
        if line.find("User time")!=-1:
            s=line.find(":")
            cpu_time += float(line[s+1:])
        elif line.find("System time")!=-1:
            s=line.find(":")
            system_time += float(line[s+1:])
            cpu_time += float(line[s+1:])
        elif line.find("Major (requiring I/O) page faults")!=-1:
            s=line.find(":")
            page_fault = float(line[s+1:]) #缺页中断的次数
    print("cpu time: {:f} s, system time: {:f} s, page fault: {:n}".format(cpu_time,system_time,page_fault))
    return cpu_time, system_time, page_fault

def exec():
    command_list = []
    mem_list = []
    cpu_time_list = []
    system_time_list = []
    page_fault_list = []
    res_list = []
    c_range = range(len(app_list))
    p_range = np.arange(1.0,0.2,-0.1).tolist()    # print("c range",c_range)
    # print("p range",p_range)
    for i in c_range:
        # max_mem = -1
        max_mem = 155
        for ratio in p_range:
            mem = -1 if max_mem==-1 else int(ratio*max_mem)

            # print(i,mem)
            full_cmd = get_cmd(i,mem)
            command_list.append(full_cmd)
            # print(full_cmd)
            popen = subprocess.Popen(full_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True) 
            stdout, stderr = popen.communicate()
            res=stdout.decode().split('\n')+stderr.decode().split('\n')
            res_list.append(res)
            # print(res)
            cpu_time, system_time, page_fault = get_data(res)
            cpu_time_list.append(cpu_time)
            system_time_list.append(system_time)
            page_fault_list.append(page_fault)

            if mem ==-1:
                f = open('/sys/fs/cgroup/memory/farmemory/memory.max_usage_in_bytes', 'r')
                mem_read = int(f.read())
                # print("mem_read:",mem_read)
                max_mem = int(mem_read/1024/1024)
                f.close()
            if mem ==-1:
                mem_list.append(max_mem)
            else:
                mem_list.append(mem)
        
            # save file
            res_filename = 'log_duye'
            f = open(res_filename,'w')
            for cmd_item,res_item in zip(command_list,res_list):
                f.write(cmd_item+'\n')
                for line in res_item:
                    f.write(line+'\n')
            f.close()
            
            full_app_list = [x for x in app_list for i in range(8)]
            save_data = pd.DataFrame({'app':full_app_list[:len(system_time_list)],'system time':system_time_list,'cpu time':cpu_time_list,'memory limit':mem_list,'page fault':page_fault_list})
            save_data.to_csv('res_duye.csv',index=False,sep=',',columns=['app','system time','cpu time','memory limit','page fault'])
    

if __name__== '__main__':
    exec()
