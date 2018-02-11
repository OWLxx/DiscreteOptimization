#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
import os
from gurobipy import *
import numpy as np

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def distance(a, b):
    return ((a.x-b.x)**2+(a.y-b.y)**2)**0.5

def gurobipysolver(facility, customer):
    demand = [i.demand for i in customer]
    capacity = [i.capacity for i in facility]
    setupCost = [i.setup_cost for i in facility]
    # print demand, capacity, setupCost
    dist = [[0 for _ in range(len(facility))] for _ in range(len(customer))]

    for i in range(len(customer)):
        for j in range(len(facility)):
            dist[i][j] = length(customer[i].location, facility[j].location)

    fac = range(len(facility))
    cus = range(len(customer))

    m = Model("facillity")
    open = m.addVars(fac, vtype=GRB.BINARY,  name='open')    #  fac open or not
    transport = m.addVars(cus, fac,vtype=GRB.BINARY,  name='dist') # cus to fac

    obj = LinExpr()
    for f in fac:
        obj += open[f]*setupCost[f]
    for c in cus:
        for f in fac:
            obj += transport[c, f]*dist[c][f]
    m.setObjective(obj, GRB.MINIMIZE)


    for f in fac:

        m.addConstr(sum([transport[c, f]*demand[c] for c in cus]) <= capacity[f]*open[f])


    for c in cus:
        m.addConstr(sum(transport[c, f] for f in fac) == 1)



    m.Params.timeLimit = 120.0
    # m.Params.IterationLimit = 15


    m.optimize()


    solution = []
    used = []
    for f in fac:
        # print f, open[f], '?'
        if open[f].x >0.99:
            used.append(1)
        else:
            used.append(0)
    for c in cus:
        for f in fac:
            if transport[c,f].x!=0:
                solution.append(f)

    return solution, used







def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    # build a trivial solution

    solution, used = gurobipysolver(facilities, customers)
    print solution
    print used
    print '#####################'
    # pack the facilities one by one until all the customers are served


    # calculate the cost of the solution
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

cwd = os.getcwd()
dir = cwd+'/data/fl_16_1'
f = open(dir)
print solve_it(f.read())

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

