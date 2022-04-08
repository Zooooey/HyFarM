import numpy as np
import matplotlib.pyplot as plt


servers_remain_cpu= [40]*8
servers_graph =[[1]*8]*8
print("servers_remain_cpu")
print(servers_remain_cpu)


def task_latency(y0, k1, turn, k2, x):
    # print(y0,k1,turn,k2,x)
    if (turn == 0 or x < turn):
        y = y0 + k1 * x
    else:
        y = y0 + k1 * turn + k2 * (x - turn)
    # print(y)
    return y


def task_latency_hybrid(y0, k1, k2, k3, turn1, turn2, x):
    # print(y0,k1,turn,k2,x)
    if (turn1 == 0 or x <= turn1):
        y = y0 + k1 * x
    elif ((x > turn1 and x <= turn2) or turn2 == 0):
        y = y0 + k1 * turn1 + k2 * (x - turn1)
    elif (x > turn2):
        y = y0 + k1 * turn1 + k2 * (turn2 - turn1) + k3 * (x - turn2)
    # print(y)
    return y



x = [0] * 11
y1 = [0] * 11
y2 = [0] * 11
y3 = [0] * 11
yy1 = [0] * 11
yy2 = [0] * 11
yy3 = [0] * 11
# y坐标轴上点的数值
for num in range(0, 11):
    x[num] = num * 0.1
    y2[num] = task_latency(10, 4, 0, 1, num)
    y3[num] = task_latency(10, 2, 8, 8, num)
    y1[num] = task_latency(10, 1, 4, 5, num)

# 第2步：使用plot绘制线条第1个参数是x的坐标值，第2个参数是y的坐标值
t = np.arange(0, 1.1, 0.1)
plt.plot(t, y2, color='r', marker='o', linestyle='dashed', label='k1=4,k2=0,turn=no')
plt.plot(t, y1, color='g', marker='o', linestyle='dashed', label='k1=1,k2=5,turn=4')
plt.plot(t, y3, color='b', marker='o', linestyle='dashed', label='k1=2,k2=8,turn=8')
plt.xlabel('far memory ratio')
plt.ylabel('latency')
plt.legend()
plt.savefig('figure\single-far.pdf')
plt.show()
#######################################################

for num in range(0,11):
    x[num] = num*0.1
    yy2[num] = task_latency_hybrid(100,0.5,7,0,8,0,num)
    yy1[num] = task_latency_hybrid(100,1,3,8,3,9,num)
    yy3[num] = task_latency_hybrid(100,2,8,3,5,8,num)

t = np.arange(0,1.1, 0.1)
plt.plot(t,yy2,color='r',marker='o',linestyle='dashed',label='k1=1,k2=7,k3=0,turn1=8,turn2=0')
plt.plot(t,yy1,color='g',marker='o',linestyle='dashed',label='k1=2,k2=3,k3=8,turn1=3,turn2=9')
plt.plot(t,yy3,color='b',marker='o',linestyle='dashed',label='k1=3,k2=8,k3=3,turn1=5,turn2=8')
plt.xlabel('far memory ratio')
plt.ylabel('latency')
plt.legend()
plt.savefig('figure/hybrid_far.pdf')
plt.show()

##################################################################################
def memory_allocation(total_size, local_mem_ratio, hfm_ratio):
    return

def vfm_ratio(total_size,a1_lm,a1_hfm):
    a1_vfm = 1-a1_lm-a1_lm
    return a1_vfm

a=0.5
S = 10 # 10G
a1 = 0.4*S
a1_lm = a
a1_hfm = 0
a1_vfm = 1-a1_lm-a1_lm
a1_y0 = 20 #20s

#一个机子上两个任务互相抢占：共有三种任务：(1)k1<k0且无turn，(2)k1>k00且无turn，(3)k1<k0且k2>k00且turn>t0, 6种情况
k0 = 2
k00= 5

yy=[0]*11

# 3 vs 3
for num in range(0,11):
    print(task_latency(10,1.5,6,8,num),task_latency(10,1.5,6,8,10-num))
    yy[num]= task_latency(10,1.5,6,8,num)*task_latency(10,1.5,6,8,10-num)
print(yy)
t = np.arange(0,1.1,0.1)
plt.plot(t,yy,color='r',marker='o',linestyle='dashed',label='type3,k2=8,turn=6')

# 3 vs 3
for num in range(0,11):
    yy[num]= task_latency(10,1.5,6,6,num)*task_latency(10,1.5,6,6,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='y',marker='o',linestyle='dashed',label='type3,k2=6,turn=6')

# 2 vs 2
for num in range(0,11):
    yy[num]= task_latency(10,6,0,8,num)*task_latency(10,6,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='g',marker='o',linestyle='dashed',label='type2,k1=6')

for num in range(0,11):
    yy[num]= task_latency(10,3,0,8,num)*task_latency(10,3,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='orange',marker='o',linestyle='dashed',label='type2,k1=3')

# 1 vs 1
for num in range(0,11):
    yy[num]= task_latency(20,2,0,8,num)*task_latency(20,2,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='b',marker='o',linestyle='dashed',label='type1,k1=2')
for num in range(0,11):
    yy[num]= task_latency(20,1.5,0,8,num)*task_latency(20,1.5,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='grey',marker='o',linestyle='dashed',label='type1,k1=1.5')
plt.xlabel('far memory ratio')
plt.ylabel('latency product')
plt.legend()
plt.savefig('figure/single-node-2-task.pdf')


##############################################################################
# 3 vs 2
for num in range(0,11):
    yy[num]= task_latency(10,1.5,6,6,num)*task_latency(10,6,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='r',marker='o',linestyle='dashed',label='3 vs 2,1_turn=6,2_k1=6')
for num in range(0,11):
    yy[num]= task_latency(10,1.5,6,6,num)*task_latency(10,3,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='orange',marker='o',linestyle='dashed',label='3 vs 2,1_turn=3,2_k1=3')

for num in range(0,11):
    yy[num]= task_latency(10,1.5,3,6,num)*task_latency(10,6,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='pink',marker='o',linestyle='dashed',label='3 vs 2, 2_k1=6')
#3 vs 1
for num in range(0,11):
    yy[num]= task_latency(10,1.5,6,6,num)*task_latency(10,1.5,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='g',marker='o',linestyle='dashed',label='3 vs 1, 1_k1=6')

for num in range(0,11):
    yy[num]= task_latency(10,1.5,3,6,num)*task_latency(10,1.5,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='grey',marker='o',linestyle='dashed',label='3 vs 1, 1_k1=3')

#1 vs 2
for num in range(0,11):
    yy[num]= task_latency(10,1.5,0,8,10-num)*task_latency(10,6,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='b',marker='o',linestyle='dashed',label='1 vs 2,2_k1=6')
for num in range(0,11):
    yy[num]= task_latency(10,1.5,0,8,10-num)*task_latency(10,3,0,8,10-num)
print(yy)
t = np.arange(0,1.1, 0.1)
plt.plot(t,yy,color='black',marker='o',linestyle='dashed',label='1 vs 2,2_k1=3')
plt.xlabel('far memory ratio')
plt.ylabel('latency product')
plt.legend()
plt.savefig('figure/2-node-2-task.pdf')