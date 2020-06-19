#coding:utf-8
import re,logging
import numpy as np
import math
from matplotlib import pyplot as plt
from itertools import islice

drawmap = {
    'title': '',
    'picname': '',
    'point': '.',
    'time': [],
    'data': {},
    'yticks': np.linspace(-1.5, 1.5, 13)
    } 

#返回nums中离target最近的数字的下标
def lower_bound(nums, target):
    low, high = 0, len(nums)-1
    pos = len(nums)
    while low<high:
        mid = (low+high)//2
        if nums[mid] < target:
            low = mid+1
        else:
            high = mid
    if low != 0 and (target - nums[low-1]) < (nums[low] - target):
            return low-1
    return low
    
def draw_pic(drawmap):
    plt.figure(figsize=(6,6))
    logging.info(len(drawmap['data']))
    for lname,line in drawmap['data'].items():
        plt.plot(drawmap['time'], line, drawmap['point'], label=lname, linewidth=1)  # 画成线
    plt.yticks(drawmap['yticks'])
    plt.legend()
    plt.title(drawmap['title'])
    plt.savefig(drawmap['picname'])
    plt.show()
    plt.close()    
    
def get_score(x,sig=0.4):
    return np.exp(-x**2/(2* sig **2))/(math.sqrt(2*math.pi)*sig)

def get_begin(l,begin):
    if begin == None:
        for i in range(len(l)):
            if l[i] != 0:
                return i
    for i in range(len(l)-1):
        if l[i] == begin and l[i+1] != begin:
            return i
    return 0

def get_bias(listenlist,readlist,begin,sig):
    length = len(readlist[0])
    datasize = len(listenlist) - 1
    lbeg = get_begin(listenlist[1],begin)
    rbeg = get_begin(readlist[1],begin)
    off_time = readlist[0][rbeg] - listenlist[0][lbeg]

    scores = [0 for i in range(datasize)]
    for rindex in range(rbeg,length):
        lindex = lower_bound(listenlist[0],readlist[0][rindex] - off_time)
        for i in range(datasize):
            scores[i] += get_score(readlist[i+1][rindex] - listenlist[i+1][lindex],sig)
    count = length - rbeg
    for i in range(datasize):
        scores[i] /= count
        logging.info("第%d项得分：%f" % (i+1,scores[i]))
        print("%d:%f" % (i+1,scores[i]))
    print(sum(scores)/datasize)
    return sum(scores)/datasize
          
def parse_cmd_vel_listen(data_topic_listen):
    with open (data_topic_listen,'r') as f:
        a = f.read()
    segs = a.replace('\n', '').split(',')
    slen = len(segs)
    segs[-1] = segs[-1].replace(']','')
    listenlist = [[] for i in range(3)]
    index = 0 
    while index < slen:
        seg = segs[index]
        time = float(segs[index+1]) - float(segs[1])
        index += 2
        pl = float(re.search('linear:\s+x:\s(\S+)', seg).group(1))
        pa = float(re.search('angular[\S\s]*z:\s(\S+)', seg).group(1))
        listenlist[0].append(time)
        listenlist[1].append(pl)
        listenlist[2].append(pa)
    return listenlist

def parse_cmd_vel_read(data_bag_read):
    with open (data_bag_read,'r') as f:
        a = f.read()
    segs = a.split('\\n')[:-1]
    bagreadlist = [[] for i in range(3)] 
    for seg in segs:
        pl = float(seg.split(',')[-2])        
        pa = float(seg.split(',')[-1])
        time = float(re.findall('(\d+\.\d+)', seg)[0])
        bagreadlist[0].append(time)
        bagreadlist[1].append(pl)
        bagreadlist[2].append(pa)
    return bagreadlist

def parse_cmd_vel(data_topic_listen,topic_listen,data_bag_read,bag_read,begin = 0,sig=0.4):
    logging.info("%s\n%s\n%s\n%s\n" % (data_topic_listen,topic_listen,data_bag_read, bag_read))
    listenlist = parse_cmd_vel_listen(data_topic_listen)
    readlist = parse_cmd_vel_read(data_bag_read)
    if len(listenlist[0]) < 2 or len(readlist[0]) < 2:
        logging.info("cmd_vel is empty")
        return 0
    
    drawmap['title'] = '/CMD_VEL'
    drawmap['point'] = '.'
    drawmap['yticks'] = np.linspace(-0.5, 2, 11)
        
    drawmap['time'] = listenlist[0]
    drawmap['data']['linear'] = listenlist[1]
    drawmap['data']['angular'] = listenlist[2]
    drawmap['picname'] = topic_listen
    draw_pic(drawmap)
    
    drawmap['time'] = readlist[0]
    drawmap['data']['linear'] = readlist[1]
    drawmap['data']['angular'] = readlist[2]
    drawmap['picname'] = bag_read
    draw_pic(drawmap)
    drawmap['data'] = {}
    
    return get_bias(listenlist,readlist,begin,sig)

def parse_speed_limit_listen(data_topic_listen):
    with open(data_topic_listen, 'r') as f:
        a = f.read()
    segs = a.split('data:')[1:]
    t0 = float(re.findall('\d+\.\d+', segs[0])[5])
    listenlist = [[] for i in range(5)]
    for seg in segs:
        numlist = re.findall('-?\d+\.\d+', seg)
        listenlist[1].append(float(numlist[1]))
        listenlist[2].append(float(numlist[2]))
        listenlist[3].append(float(numlist[3]))
        listenlist[4].append(float(numlist[4]))
        listenlist[0].append(float(numlist[5]) - t0)
    return listenlist

def parse_speed_limit_read(data_bag_read):
    with open(data_bag_read, 'r') as f:
        a = f.read()
    segs = a.split('data:')[1:]
    t0 = re.search('Time\[(\d+)', segs[0]).group(1)
    bagreadlist = [[] for i in range(5)]
    for seg in segs:
        numlist = re.findall('-?\d+\.\d+', seg)
        #评分时以时间后第一组数据做起点校验
        bagreadlist[1].append(float(numlist[2]))
        bagreadlist[2].append(float(numlist[1]))
        bagreadlist[3].append(float(numlist[3]))
        bagreadlist[4].append(float(numlist[4]))
        t = re.search('Time\[(\d+)', seg).group(1)
        bagreadlist[0].append((int(t) - int(t0)) / 1000000000.)
    return bagreadlist

def parse_speed_limit(data_topic_listen,topic_listen,data_bag_read,bag_read,begin = 0,sig=0.4):
    logging.info("%s\n%s\n%s\n%s\n" % (data_topic_listen,topic_listen,data_bag_read, bag_read))
    listenlist = parse_speed_limit_listen(data_topic_listen)
    readlist = parse_speed_limit_read(data_bag_read)
    if len(listenlist[0]) < 2 or len(readlist[0]) < 2:
        logging.info("speed_limit is empty")
        return 0
    
    drawmap['title'] = '/SPEED_LIMIT'
    drawmap['point'] = '.'
    drawmap['yticks'] = np.linspace(-1.5, 1.5, 13)
    
    drawmap['time'] = listenlist[0]
    drawmap['data']['linearmin'] = listenlist[1]
    drawmap['data']['linearmax'] = listenlist[2]
    drawmap['data']['angularmin'] = listenlist[3]
    drawmap['data']['angularmax'] = listenlist[4]
    drawmap['picname'] = topic_listen
    draw_pic(drawmap)
    
    drawmap['time'] = readlist[0]
    drawmap['data']['linearmin'] = readlist[2]
    drawmap['data']['linearmax'] = readlist[1]
    drawmap['data']['angularmin'] = readlist[3]
    drawmap['data']['angularmax'] = readlist[4]
    drawmap['picname'] = bag_read
    draw_pic(drawmap)
    drawmap['data'] = {}
    
    return get_bias(listenlist,readlist,begin,sig)

def parse_platform_guardian_listen(data_topic_listen):
    listenlist = [[] for i in range(13)]

    with open(data_topic_listen, 'rb') as f:
        a = f.read()
    segs = re.split('data: \[',a.decode())
    for seg in segs[2:]:
        dataline = re.findall('\d', seg)
        for i in range(1,13):
            num = int(dataline[i-1])
            if num == 0:
                listenlist[i].append(0)
            else:
                listenlist[i].append(2*(i-1)+num)
    
    segs = re.split('\], ', a.decode())
    t0 = re.match('(\d+\.\d+)', segs[2]).group(1)
    for seg in segs[2:]:
        t = re.match('(\d+\.\d+)', seg).group(1)
        listenlist[0].append(float(t) - float(t0))
        
    return listenlist

def parse_platform_guardian_read(data_bag_read):
    bagreadlist = [[] for i in range(13)]
    with open(data_bag_read, 'r') as f:
        a = f.read()
    segs = re.split('data: \[', a)
    t0 = re.findall('\d+', segs[1])[12]
    for seg in islice(segs,1,None):        
        dataline = re.findall('\d+', seg)
        time = dataline[12]
        bagreadlist[0].append(float((int(time) - int(t0)) / 1000000000))
        for i in range(1,13):
            num = int(dataline[i-1])
            if num == 0:
                bagreadlist[i].append(0)
            else:
                bagreadlist[i].append(2*(i-1)+num)
                
    return bagreadlist

def parse_platform_guardian(data_topic_listen,topic_listen,data_bag_read,bag_read,begin = None,sig=0.4):
    logging.info("%s\n%s\n%s\n%s\n" % (data_topic_listen,topic_listen,data_bag_read, bag_read))
    listenlist = parse_platform_guardian_listen(data_topic_listen)
    readlist = parse_platform_guardian_read(data_bag_read)
    if len(listenlist[0]) < 2 or len(readlist[0]) < 2:
        logging.info("speed_limit is empty")
        return 0
    drawmap['title'] = '/PLATFORM/PLATFORM_GUARDIAN'
    drawmap['point'] = '1'
    drawmap['yticks'] = range(0, 26, 2)
    
    drawmap['time'] = listenlist[0]
    for i in range(1,13):
        key = 'ultrasound%d'%i
        drawmap['data'][key] = listenlist[i]
    drawmap['picname'] = topic_listen
    draw_pic(drawmap)
    
    drawmap['time'] = readlist[0]
    for i in range(1,13):
        key = 'ultrasound%d'%i
        drawmap['data'][key] = readlist[i]
    drawmap['picname'] = bag_read
    draw_pic(drawmap)
    drawmap['data'] = {}
    
    return get_bias(listenlist,readlist,begin,sig)

parse_topic_function = {
    '/cmd_vel': parse_cmd_vel,
    '/chassis/speed_limit' : parse_speed_limit,
    '/platform/platform_guardian': parse_platform_guardian
}