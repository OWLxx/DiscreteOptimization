from gurobipy import *

siteNames = ["Reno", "South Lake Tahoe", "Carson City", "Garnerville",
              "Fernerly", "Tahoe City", "Incline Village", "Truckee"]
sites = range(len(siteNames))
clients = sites[1:]
demand = [ 1000, 1200, 1600, 1400, 1200, 1000, 1700]
dist = [[0, 59.3, 31.6, 47.8, 34.2, 47.1, 36.1, 31.9],
        [62.2, 0, 27.9, 21.0, 77.5, 30.0, 27.1, 44.7],
        [32.2, 27.7, 0, 16.2, 50.0, 39.4, 24.9, 42.6],
        [50.7, 21.0, 16.4, 0, 66.1, 49.7, 35.2, 52.9],
        [34.4, 77.4, 49.6, 65.9, 0, 80.8, 67.1, 65.5],
        [46.9, 30.1, 39.6, 49.7, 80.5, 0, 14.4, 15.0],
        [36.9, 27.1, 25.2, 35.2, 67.1, 14.4, 0, 17.6],
        [31.9, 44.7, 62.8, 52.8, 65.6, 15.0, 17.6, 0]]
capacity = 4500

model = Model('Diesel Fuel Delivery')

x = {}
for i in sites:
    for j in sites:
        x[i,j] = model.addVar(vtype=GRB.BINARY)

u = {}
for i in clients:
    u[i] = model.addVar(lb=demand[i], ub=capacity)

model.update()

obj = quicksum( dist[i][j]*x[i,j] for i in sites for j in sites if i != j )
model.setObjective(obj)

for j in clients:
    model.addConstr(quicksum( x[i,j] for i in sites if i != j ) == 1)
for i in clients:
    model.addConstr(quicksum( x[i,j] for j in sites if i != j ) == 1)

for i in clients:
    model.addConstr(u[i] <= capacity + (demand[i] - capacity)*x[0,i])

for i in clients:
    for j in clients:
        if i != j:
            model.addConstr(u[i] - u[j] + capacity*x[i,j] <= capacity - quant[j])

model.optimize()