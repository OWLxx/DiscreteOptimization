#!/usr/bin/python
# -*- coding: utf-8 -*-
from gurobipy import *
import google
import math
import os
from collections import namedtuple
import math
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def distance(x1, y1, x2, y2):
    # Manhattan distance
    dist = (abs(x1 - x2)**2 + abs(y1 - y2)**2)**0.5

    return dist

def main(data, num_vehicles,vehicle_capacity ):
  # Create the data.
  #data = create_data_array()
  locations = data[0]
  demands = data[1]
  num_locations = len(locations)
  depot = 0    # The depot is the start and end point of each route.


  # Create routing model.
  if num_locations > 0:
    routing = pywrapcp.RoutingModel(num_locations, num_vehicles, depot)
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

    # Setting first solution heuristic: the
    # method for finding a first solution to the problem.
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # The 'PATH_CHEAPEST_ARC' method does the following:
    # Starting from a route "start" node, connect it to the node which produces the
    # cheapest route segment, then extend the route by iterating on the last
    # node added to the route.

    # Put a callback to the distance function here. The callback takes two
    # arguments (the from and to node indices) and returns the distance between
    # these nodes.

    dist_between_locations = CreateDistanceCallback(locations)
    dist_callback = dist_between_locations.Distance
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)

    # Put a callback to the demands.
    demands_at_locations = CreateDemandCallback(demands)
    demands_callback = demands_at_locations.Demand

    # Add a dimension for demand.
    slack_max = 0
    fix_start_cumul_to_zero = True
    demand = "Demand"
    routing.AddDimension(demands_callback, slack_max, vehicle_capacity,
                         fix_start_cumul_to_zero, demand)

    # Solve, displays a solution if any.
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
          # Display solution.
          # Solution cost.
          print( "Total distance of all routes: " + str(assignment.ObjectiveValue()) + "\n")
          total_tour = []
          for vehicle_nbr in range(num_vehicles):
                index = routing.Start(vehicle_nbr)
                index_next = assignment.Value(routing.NextVar(index))
                route = ''
                route_dist = 0
                route_demand = 0
                while not routing.IsEnd(index_next):
                    node_index = routing.IndexToNode(index)
                    node_index_next = routing.IndexToNode(index_next)
                    route += str(node_index) + " -> "
                    # Add the distance to the next node.
                    route_dist += dist_callback(node_index, node_index_next)
                    # Add demand.
                    route_demand += demands[node_index_next]
                    index = index_next
                    index_next = assignment.Value(routing.NextVar(index))
                node_index = routing.IndexToNode(index)
                node_index_next = routing.IndexToNode(index_next)
                route += str(node_index) + " -> " + str(node_index_next)


                route_dist += dist_callback(node_index, node_index_next)
                temp = route.split('->')
                temp = [int(i) for i in temp if i != 0]
                total_tour.append(temp)
                print ("Route for vehicle " + str(vehicle_nbr) + ":\n\n" + route + "\n")
                print ("Distance of route " + str(vehicle_nbr) + ": " + str(route_dist))
                print ("Demand met by vehicle " + str(vehicle_nbr) + ": " + str(route_demand) + "\n")
          return total_tour
    else:
        print ('No solution found.')
  else:
    print ('Specify an instance greater than 0.')



class CreateDistanceCallback(object):
  """Create callback to calculate distances between points."""

  def __init__(self, locations):
    """Initialize distance array."""
    size = len(locations)
    self.matrix = {}

    for from_node in range(size):
      self.matrix[from_node] = {}
      for to_node in range(size):
        x1 = locations[from_node][0]
        y1 = locations[from_node][1]
        x2 = locations[to_node][0]
        y2 = locations[to_node][1]
        self.matrix[from_node][to_node] = distance(x1, y1, x2, y2)

  def Distance(self, from_node, to_node):
    return self.matrix[from_node][to_node]

class CreateDemandCallback(object):
  """Create callback to get demands at each location."""

  def __init__(self, demands):
    self.matrix = demands

  def Demand(self, from_node, to_node):
    return self.matrix[from_node]

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    locations = []
    demands = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))
        locations.append([float(parts[1]), float(parts[2])])
        demands.append(int(parts[0]))


    #the depot is always the first customer in the input
    depot = customers[0]
    total_tour = main([locations, demands], vehicle_count, vehicle_capacity)
    total_tour = [i[1:-1] for i in total_tour]
    # print(total_tour, '!!!!!!!!!!!!!')
    vehicle_tours = []
    for t in total_tour:
        if t == []:
            vehicle_tours.append([])
        else:
            temp = []
            for i in t:
                temp.append(customers[i])
            vehicle_tours.append(temp)
    print(vehicle_tours, '!!!!!!!!!!!')







    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands

    






    print(vehicle_tours, '############')  # this is the return type
    # [[custom1, custom2,...] [custom3, custom4, ...]]

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot,vehicle_tour[0])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(vehicle_tour[i],vehicle_tour[i+1])
            obj += length(vehicle_tour[-1],depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    return outputData

cur = os.getcwd()
datawd = cur+'\data\\vrp_484_19_1'
print(datawd)
f = open(datawd)
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

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

