#!/usr/bin/python
# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import math
import os
import random
import numpy as np
import scipy
from collections import namedtuple
import sklearn
import collections
from sklearn.cluster import KMeans


Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def plot(points, solution, order):
    x = [p.x for p in points]
    y = [p.y for p in points]
    plt.plot(x,y , 'ro', markersize=15)
    if solution==[]: solution = range(len(x))
    for i in range(len(solution)):
        if i==0:
            xt = [x[solution[-1]], x[solution[0]]]
            yt = [y[solution[-1]], y[solution[0]]]
            plt.plot(xt, yt, c='k')
        else:
            xt = [x[solution[i-1]], x[solution[i]]]
            yt = [y[solution[i-1]], y[solution[i]]]
            plt.plot(xt, yt, c='k')
            s = ' '.join([str(i) for i in order])
            plt.title (s)

    plt.show()
    plt.close()

def kmean(points):
    numberofCluster = int(len(points)/1800) +1
    number = [[int(i.x), int(i.y)] for i in points]
    number = np.array(number)
    kmeans = KMeans(n_clusters=numberofCluster).fit(number)
    label = kmeans.labels_
    center = kmeans.cluster_centers_
    ans = [[] for _ in range(numberofCluster)]
    for i in range(len(label)):
        ans[label[i]].append(i)


    # plt.figure(1)
    # color = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    # for i in range(len(label)):
    #     c = color[label[i]]
    #     plt.scatter(points[i].x, points[i].y, color = c)
    # plt.show()
    return ans







def total_length(points, solution):
    ans = 0
    for i in range(len(solution)):
        if i==len(solution)-1:
            ans += length(points[solution[0]], points[solution[i]])
        else:
            ans += length(points[solution[i]], points[solution[i+1]])
    return ans

def greedyInitial(points, curorder):
    route = []
    unused = curorder
    temp = [points[i].x+points[i].y for i in unused]
    index = temp.index(max(temp))
    print(len(unused), index, '?')
    route.append(unused[index])
    unused.pop(index)
    pre = index
    while unused:
        nnext = [length(points[pre], points[i]) for i in unused]
        cur = nnext.index(min(nnext))
        cur = unused[cur]
        pre = cur
        route.append(cur)
        # print(cur, unused)
        unused = [i for i in unused if i!=cur]
    return route





def kopt(points, order):
    # order = list(range(len(points))) # py3 range is generator
    # plot(points, order, order)
    minorder = []
    minlen = float('inf')
    unused = order[:]
    while unused:
        i = unused.pop(0)
        i_normalize = order.index(i)
        count = 0
        Tabu = [i]
        Tabu.append(order[(i_normalize+1,0)[i_normalize==len(order)-1]])
        while count==0 or cur!=order[(i_normalize,0)[i_normalize==len(order)]]:
            Tabu.append(order[(i_normalize,0)[i_normalize==len(order)]])
            count += 1
            cur = order[i_normalize]
            curnext = order[(i_normalize+1,0)[i_normalize==len(order)-1]]

            for j in range(len(order)):
                J = order[j]
                Jnext = order[(j+1, 0)[j==len(order)-1]]
                # if order[j] not in Tabu and order[j]!=order[(curnext+1, 0)[curnext==len(order)-1]]:
                if order[j] not in Tabu:
                    Tabu.append(order[j])
                    a = length(points[cur], points[curnext])    # i->i.next
                    b = length(points[J], points[Jnext])     # j-> j.next
                    c = length(points[cur], points[J])   #  i ->j
                    d = length(points[curnext], points[Jnext])  # i.next -> j.next
                    if c+d < a+b:
                        if i_normalize+1<j:
                            order[i_normalize+1:j+1] = order[i_normalize+1:j+1][::-1]
                        else:
                            order[j+1:i_normalize+1] = order[j+1:i_normalize+1][::-1]
                        curlen = total_length(points, order)
                        # plot(points, order, order)
                        if curlen < minlen:
                            minorder = order[:]
                            minlen = curlen
                        break
    print('final of this turn', minlen, minorder)
    return minorder, minlen







def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    x = [x[0] for x in points]
    y = [x[1] for x in points]
    kmean(points)


    # build a trivial solution
    # visit the nodes in the order they appear in the file
    if len(points) <=2000:
        order, cursum  = kopt(points, list(range(len(points))))
        solution = order[:]

        while True:
            presum = cursum
            temp, cursum = kopt(points, order)[:]
            if cursum < presum:
                print(cursum, presum, '########')
                order = [i for i in temp]
                order = order[:]
                solution = [i for i in temp]
                solution = solution[:]
                print('temp', temp)
                print('solution', solution)
            else:
                break
        a = total_length(points, solution)

        # solution = [0, 6,5,1,2,3,4,7,8,9,10,11]
        ####################################################
        # plt.plot(x,y , 'ro', markersize=15)
        # if solution==[]: solution = range(len(x))
        # for i in range(len(solution)):
        #     if i==0:
        #         xt = [x[solution[-1]], x[solution[0]]]
        #         yt = [y[solution[-1]], y[solution[0]]]
        #         plt.plot(xt, yt, c='k')
        #     else:
        #         xt = [x[solution[i-1]], x[solution[i]]]
        #         yt = [y[solution[i-1]], y[solution[i]]]
        #         plt.plot(xt, yt, c='k')
        #
        # plt.show()
    else:
        cluster_point = kmean(points)  # cluster_point is the index of point
        order = []
        for curcluster in cluster_point:
            curini = greedyInitial(points, curcluster)
            curord,_ = kopt(points, curini)
            order.append(curord)
        ans = []
        curcluster = order.pop()
        ans.extend(curcluster)
        while order:
            point1 = points[curcluster[-1]]
            nextindex = min([i for i in range(len(order))], key=lambda x: length(point1, points[order[x][0]]))
            curcluster = order.pop(nextindex)
            ans.extend(curcluster)
        order = ans[:]







    solution = order
    print(solution)
    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount-1):
        obj += length(points[solution[index]], points[solution[index+1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data
import sys

curdir = os.getcwd()
dir = curdir + '/data/tsp_1060_1'
f = open(dir)
solve_it(f.read())

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

