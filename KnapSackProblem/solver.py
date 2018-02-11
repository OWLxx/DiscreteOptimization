#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import numpy as np
Item = namedtuple("Item", ['index', 'value', 'weight'])

def dynamicprogramming(capacity, item_count, items):
        # print(item_count,len(items) ,'###')
        # print(items)
        dp = [[0 for _ in range(capacity+1)] for _ in range(item_count)]
        #print(dp)
        for i in range(len(items)):
            #print (i)
            for j in range(1,capacity+1):
                if i==0:
                    if j>=items[i].weight:
                        dp[i][j] = items[i].value
                else:
                    choice = 0
                    if j-items[i].weight>=0:
                        choice = dp[i-1][j-items[i].weight] + items[i].value
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1], choice)
        # print(np.array(dp))
        value = dp[-1][-1]
        indices = set()
        i = item_count-1
        target = dp[-1][-1]
        j = -1
        print('checkpoint1')
        while i >=0:  # find which item to take
            while i>0 and dp[i-1][j]==target:
                i -= 1
            indices.add(items[i].index)
            target -= items[i].value
            if target==0: break
            while True:
                if target in dp[i]:
                    j = dp[i].index(target)
                    break
                elif i <=0:
                    break
                else:
                    i -= 1

        if i==0: indices.add(items[0].index)
        print(indices)
        taken = []
        for i in range(len(items)):
            if i in indices:
                taken.append('1')
            else:
                taken.append('0')
        return value, taken, indices

def greedy(capacity, item_count, items):
    # print(items)
    items = [i for i in items if i.weight<=capacity]
    items.sort(key=lambda x: x.value/x.weight)
    items = items[::-1]

    indices = [0]*item_count
    weight = 0
    value = 0
    ic = 0
    picked = []
    for ic in range(len(items)):
        if weight+ items[ic].weight <= capacity:
            weight += items[ic].weight
            picked.append(items[ic].index)
            value += items[ic].value
    print(picked)
    return value, picked

def commbination_of_search(capacity, item_count, items):
    '''
    Start with greedy result
    Add one or two limited discrepancy search

    '''
    print(items)
    items = [i for i in items if i.weight<=capacity]
    items.sort(key=lambda x: x.value/x.weight)
    maxvalue, maxpicked = greedy(capacity, item_count, items)
    picked = maxpicked
    for ele in picked:
        tempitems = [i for i in items if i.index!=ele]
        valuetemp, picked_temp = greedy(capacity, len(tempitems), tempitems)
        if valuetemp>maxvalue:
            maxvalue = valuetemp
            maxpicked = picked_temp
    return maxvalue, maxpicked




def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    for i in range(1, item_count+1):
            line = lines[i]
            parts = line.split()
            items.append(Item(i-1, int(parts[0]), int(parts[1])))
    items.sort(key=lambda x:x.weight)

    value = 0
    weight = 0
    taken = [0]*len(items)


    if len(items)<=100:
        value, taken, _ = dynamicprogramming(capacity, item_count, items)
    elif len(items)<=0:
        print(len(items), 'length of items')
        pre = used = 30
        tempitems = items[:used]
        print(len(tempitems), 'length of tempitems')
        value, taken, indices = dynamicprogramming(capacity, len(tempitems), tempitems)
        tempitems = [i for i in items if i.index in indices]
        while len(tempitems)<30 and pre<item_count:
            used += (30-len(tempitems))
            tempitems = tempitems + items[pre:used]
            print(len(tempitems), 'length of tempitems')
            value, taken, indices = dynamicprogramming(capacity, len(tempitems), tempitems)
            tempitems = [i for i in items if i.index in indices]
            pre = used
    else:
        value, picked = commbination_of_search(capacity,len(items), items )
        for i in range(len(taken)):
            if i in picked:
                taken[i] = 1


    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

import os
cwd = os.getcwd()

f = open(cwd+'\data\ks_400_0')
print(solve_it(f.read()))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

