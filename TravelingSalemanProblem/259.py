def threeSumSmaller(nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        nums.sort()
        def dfs(nums, start, target, cur, ans):
            if len(cur)==3:
                if sum(cur) < target:
                    ans.append(cur)
                    cur = []
                else:
                    cur = []
            elif start < len(nums):
                for i in range(start, len(nums)):
                    if sum(cur) + nums[i] < target:
                        dfs(nums, i+1, target-nums[i], cur+[nums[i]], ans)
                    else:
                        break
            else:
                return
        ans = []
        dfs(nums, 0, target, [], ans)
        return len(ans)

nums = [-2, 0, 1, 3]
target = 2
threeSumSmaller(nums, target)