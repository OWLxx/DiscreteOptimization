#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import Popen, PIPE
import pickle
import math

# from numpy import array
# from scipy.cluster.vq import kmeans, vq


SUBPROBLEM = 'cluster/problem/subproblem.{0}.txt'
SUBSOLUTION = 'cluster/solution/subproblem.{0}.sol'
CLUSTER_CONTEXT = 'cluster/cluster.context.bin'


def perr(*args):
    sys.stderr.write(' '.join(map(str, args)) + '\n')


def indices(x, xs):
    return [i for i in range(len(xs)) if xs[i] == x]


def saveContext(name, customers, centroids, idx, clusterIndices):
    data = customers, centroids, idx, clusterIndices
    pickle.dump(data, open(name, 'w'))


def loadContext(name):
    return pickle.load(open(name))


def solveTSPInParts(customers, N, V):
    def makedist(xs):
        def dist(i, j):
            ax, ay = xs[i]
            bx, by = xs[j]
            dx, dy = ax - bx, ay - by
            return math.sqrt(dx ** 2 + dy ** 2)
        return dist

    customersDist = makedist(customers)

    def cost(solution):
        c = 0.0
        for i in range(len(solution)):
            j = (i + 1) % len(solution)
            c += customersDist(solution[i], solution[j])
            # perr(c)
        # perr(c)
        return c

    customers1, centroids, idx, clusterIndices = loadContext(CLUSTER_CONTEXT)

    solution = []
    reorderedClusterIndices = []
    for i, v in enumerate(clusterIndices):
        filename = SUBSOLUTION.format(i)
        order = map(int, open(filename).read().splitlines()[1].split())
        reordered = [v[x] for x in order]
        reorderedClusterIndices.append(reordered)
        solution.extend(reordered)


    def nearestCluster(clusterId, clusters):
        '''Find nearest cluster to clusterId'''
        minPair, minCost = None, None
        for otherCluster in range(len(clusters)):
            if otherCluster == clusterId:
                continue
            minPair, minCost = None, None
            for i in range(len(clusters[clusterId]) - 1):
                for j in range(len(clusters[otherCluster]) - 1):
                    fromA = clusters[clusterId][i]
                    fromB = clusters[clusterId][i + 1]
                    toA = clusters[otherCluster][j]
                    toB = clusters[otherCluster][j + 1]
                    delta = (- customersDist(fromA, fromB)
                             - customersDist(toA, toB)
                             + customersDist(fromA, toA)
                             + customersDist(fromB, toB))
                    if (minCost is None) or (delta < minCost):
                        minCost = delta
                        minPair = clusterId, otherCluster, i, j
                        # minPair = clusterId, otherCluster, i, j, delta, fromA, toA, customers[fromA], customers[fromB], customers[toA], customers[toB]
            # print('min pair for cluster {0}: {1}'.format(otherCluster, minPair))
        return minPair

    def mergeClusters(clusters, clusterFrom, clusterTo, i, j):
        '''Merge two selected clusters and return new list of clusters'''
        merged = []
        rFrom, rTo = clusters[clusterFrom], clusters[clusterTo]
        merged.extend(rFrom[:i + 1])
        merged.extend(reversed(rTo[:j + 1]))
        merged.extend(reversed(rTo[j + 1:]))
        merged.extend(rFrom[i + 1:])
        newClusters = [merged]
        for k, v in enumerate(clusters):
            if (k != clusterFrom) and (k != clusterTo):
                newClusters.append(v)
        return newClusters

    # mergingClusters = copy.deepcopy(reorderedClusterIndices)
    mergingClusters = reorderedClusterIndices
    for i in range(len(mergingClusters) - 1):
        perr('Merge {0}, len {1}'.format(i, len(mergingClusters)))
        nearest = nearestCluster(0, mergingClusters)
        mergingClusters = mergeClusters(mergingClusters, *nearest)

    solution = mergingClusters[0]


    sol = '{0} 0\n{1}'.format(cost(solution), ' '.join(map(str, solution)))
    return sol


def solveIt(inputData):
    # return open('sol').read()

    lines = inputData.split('\n')

    N = int(lines[0])
    customers = []
    for i in range(1, N+1):
        pair = map(float, lines[i].split())
        customers.append((pair[0], pair[1]))

    V = 4
    return solveTSPInParts(customers, N, V)

    return open('5.sol').read()
    # Writes the inputData to a temporay file

    tmpFileName = 'tmp.data'
    tmpFile = open(tmpFileName, 'w')
    tmpFile.write(inputData)
    tmpFile.close()

    # Runs the command: java Solver -file=tmp.data

    #process = Popen(['go', 'run', 'solver.go', tmpFileName], stdout=PIPE)
    process = Popen(['./wrapper.sh', tmpFileName], stdout=PIPE)
    #process = Popen(['./wrapper.sh', 'data/gc_500_1'], stdout=PIPE)
    (stdout, stderr) = process.communicate()

    # removes the temporay file

    os.remove(tmpFileName)

    return stdout.strip()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print( solveIt(inputData))
    else:
        print ('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
