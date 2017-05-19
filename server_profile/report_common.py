
#-*- coding: utf-8 -*-

"""
绘制action图形
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import re

def draw_graph(dataList, xLabel, yLabel, title):

    plt.rc('text', usetex=False)
    #plt.rc('font', family='serif')

    for data in dataList:
        # TODO:标记
        # TODO:颜色
        line = plt.plot(data[2], data[3])
        print( line )

    plt.ylabel(yLabel)
    plt.xlabel(xLabel,fontsize=16)

    plt.title(title,fontsize=16, color='r')

    # Make room for the ridiculously large title.
    plt.subplots_adjust(top=0.8)
    plt.grid()

    #plt.savefig('tex_demo')
    plt.show()

#scanRe = re.compile( r"(?P<time>\d+)\s+" )
scanRe = re.compile( r"(?P<time>[-+]?[0-9]*\.?[0-9]+)\n" )

def read_action_data(actName, idx):
    fileName = actName

    fileObj = open(fileName, 'r')

    y = []
    x = []
    idx = 1

    for line in fileObj.readlines():
        #print(line)
        tmp = scanRe.match(line)
        if(tmp==None):
            continue;

        y.append(float(tmp.group("time")))
        x.append(idx); idx+=60

    return (actName, idx, x, y)

def draw_action_figure(dataFile, xLable, yLable, title):
    data = []
    idx = 0
    d1 = read_action_data(dataFile, idx);
    data.append(d1)
    draw_graph( data, u'running time', u'cpu', u'gs server')

