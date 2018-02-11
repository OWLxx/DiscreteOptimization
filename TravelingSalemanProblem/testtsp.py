import tsp
t = tsp([(0,0), (0,1), (1,0), (1,1)])
t.solve()
print(t.result)