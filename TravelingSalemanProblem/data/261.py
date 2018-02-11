import  collections
def validTree(n, edges):

        neighbor = collections.defaultdict(list)
        for i in edges:
            neighbor[i[0]].append(i[1])
            neighbor[i[1]].append(i[0])

        def dfs(node, target, step):
            for n in neighbor[node]:
                if n != target:
                    if not dfs(n, target, step+1):
                        return False
                elif n==target and step==1:
                    continue
                else:
                    return False
            return True


        for i in range(n):
            if not dfs(i, i, 0):
                return False

        return True

n = 5
edges = [[0,1],[0,2],[2,3],[2,4]]

validTree(n, edges)