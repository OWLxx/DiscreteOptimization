import collections

def wordPatternMatch(pattern, str):


        def issame(str, dic, length):
            for k, v in dic.items():
                if not all(str[i:i+length[k]]==str[v[0]:v[0]+length[k]] for i in v):
                    return False
            return True

        def findmaxindex(str, dic, length):
            space = 0
            for k, l in dic.items():
                for i in l:
                    if i==-1:
                        if length[k] != 0:
                            space += length[k]
                        else:
                            space += 1

            print(length, space, '???')
            return length[0] - space


        def dfs(str, curpat, minindex, maxindex, dic, length, unsigned):
            if minindex >= length[0] or curpat>=len(pattern):
                return issame(str, dic, length)
            else:
                print (curpat, minindex, maxindex, dic, length)
                if unsigned == 1 and length[pattern[curpat]] == 0:
                    if (maxindex-minindex)%len(pattern[curpat]) == 0:
                        length[pattern[curpat]] = (maxindex-minindex) / len(dic[pattern[curpat]])
                    else:
                        return False

                if length[pattern[curpat]] == 0:
                    for i in range(minindex+1, maxindex):  # i is end index
                        for j in range(len(dic[pattern[curpat]])):
                            if dic[pattern[curpat]][j]==-1:
                                dic[pattern[curpat]][j] = minindex
                                break
                        length[pattern[curpat]] = i - minindex
                        if dfs(str, curpat+1, i, findmaxindex(str, dic, length), dic, length, unsigned - 1 ):
                            return True

                else:
                    for i in range(len(dic[pattern[curpat]])):
                        if dic[pattern[curpat]][i] == -1:
                            dic[pattern[curpat]][i] = minindex
                    if dfs(str, curpat+1, minindex+length[pattern[curpat]], min(length[0], maxindex+length[pattern[curpat]]), dic, length, unsigned ):
                        return True

        length = collections.defaultdict(int)  # save length of different character
        length[0] = len(str)
        dic = collections.defaultdict(list) # save start point of current pattern
        for c, i in enumerate(pattern):
            length[i]
            dic[i].append(-1)
        if dfs(str, 0, 0, findmaxindex(str, dic, length), dic, length, len(dic) ):
            return True
        return False

pattern = "abab"
str = "redblueredblue"
wordPatternMatch(pattern, str)