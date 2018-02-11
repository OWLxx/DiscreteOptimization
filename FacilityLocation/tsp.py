
#!/usr/bin/python
# Copyright 2017, Gurobi Optimization, Inc.
# Solve a traveling salesman problem on a randomly generated set of
# points using lazy constraints. The base MIP model only includes
# 'degree-2' constraints, requiring each node to have exactly
# two incident edges. Solutions to this model may contain subtours -
# tours that don't visit every city. The lazy constraint callback
# adds new constraints to cut them off.
