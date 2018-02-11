#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections
import time

class graphnode(object):
    def __init__(self, x):
        self.val = x
        self.color = None
        self.neighbor = set()  # node inside
        self.uncolorneighbor = set() # node inside
        self.neighborcolor = set() # color inside

    def addcolor(self, color):
        if color not in self.neighborcolor:
            self.color = color
            for node in self.neighbor:
                node.neighborcolor.add(color)
            for node in self.uncolorneighbor:
                node.uncolorneighbor.discard(self)
            return True
        else:
            return False

    def delcolor(self):
        for node in self.neighbor:
            node.neighborcolor.pop(self.color)
            node.uncolorneighbor.add(self)
        self.color = None
def coloring(cur, uncolored, graph, node_count, cmp, curoutput, maxiter):
    if not uncolored:
        solution = []
        for i in range(node_count):
            solution.append(graph[i].color)
        if max(solution)<cmp:
            curoutput = solution
        return max(solution), solution
    else:
        if maxiter>0:
            uncolored.discard(cur)
            curnode = graph[cur]
            for c in range(node_count):  # add color to current node
                if curnode.addcolor(c):
                    break
            nextloop = sorted(curnode.uncolorneighbor, key=lambda x: len(x.uncolorneighbor))[-4:]
            if nextloop==[]: nextloop = sorted(uncolored, key=lambda x:len(graph[x].uncolorneighbor))[-4:]
            for node in  nextloop:
                coloring(node.val, uncolored, graph, node_count, cmp, curoutput, maxiter-1)
        else:
            uncolored.discard(cur)
            curnode = graph[cur]
            for c in range(node_count):  # add color to current node
                if curnode.addcolor(c):
                    break
            nextloop = []
            try:
                nextloop = sorted(curnode.uncolorneighbor, key=lambda x: len(x.uncolorneighbor))[-1]
            except IndexError:
                pass
            if nextloop == []:
                if uncolored:
                    nextloop = sorted(uncolored, key=lambda x:len(graph[x].uncolorneighbor))[-1]
                    # print(nextloop)
                    coloring(nextloop, uncolored, graph, node_count, cmp, curoutput, 0)






def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    graph = collections.defaultdict(list)
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        parts = [int(i) for i in parts]
        if parts[0] not in graph:
            graph[parts[0]] = graphnode(parts[0])
        if parts[1] not in graph:
            graph[parts[1]] = graphnode(parts[1])
        graph[parts[0]].neighbor.add(graph[parts[1]])
        graph[parts[0]].uncolorneighbor.add(graph[parts[1]])
        graph[parts[1]].neighbor.add(graph[parts[0]])
        graph[parts[1]].uncolorneighbor.add(graph[parts[0]])

    # print('input graph', graph)

    # sort by length
    nodeindex = sorted(graph.keys(), key=lambda x:len(graph[x].neighbor))[::-1]
    # print(nodes)

    cmp = node_count
    curoutput = []
    timeout = time.time() + 60*2  # maximum 2 minites

    uncolored = set(graph.keys())
    maxiter = 4



    a, solution = coloring(nodeindex[0], uncolored, graph, node_count, cmp, curoutput, maxiter)
    print(solution)


    # for i in range(5):
    #     stack = [nodeindex[i]]
    #
    #     # while stack and time.time()<timeout:
    #     while stack:
    #         cur = stack.pop()
    #         uncolored.discard(cur)
    #         curnode = graph[cur]
    #         for c in range(node_count):  # add color to current node
    #             if curnode.addcolor(c):
    #                 break
    #
    #         temp = sorted(curnode.uncolorneighbor, key=lambda x: len(x.uncolorneighbor))
    #         if temp != []:
    #             # print(temp)
    #             stack.append(temp[-1].val)
    #         else:
    #             temp2 = sorted(uncolored, key=lambda x:len(graph[x].uncolorneighbor))
    #             if temp2 != []:
    #                 stack.append(temp2[-1])
    #
    #     solution = []

        # for i in range(node_count):
        #     solution.append(graph[i].color)
        # if max(solution)<cmp:
        #     curoutput = solution

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

import os
temp = (os.getcwd())
temp = temp+'\data\gc_20_9'

f = open(temp)
print(solve_it(f.read()))

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

