class Solution1:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        subset = []
        def dfs(i):
            #base case: reach the end of decision tree (completed set)
            if i >= len(nums):
                res.append(subset[:]) #add copy to keep modifying subset
                return 
            
            #decision to choose nums[i]
            subset.append(nums[i])
            dfs(i+1)
            #decision not to choose nums[i], still go to next step
            subset.pop()
            dfs(i+1)
        dfs(0)
        return res
nums = [1,2,3,4]
print(Solution1.subsets(Solution1, nums))