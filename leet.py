
def longestConsecutive(nums: list[int]) -> int:
    #Sort and count the highest
    nums.sort()
    if len(nums) == 0:
        return 0
    max = 1
    temp = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]+1: 
            temp+=1
        elif nums[i] == nums[i-1]:
            continue
        else:
            temp = 1 #reset
        if temp > max:
            max = temp
    print(max)
    return max
nums = [100,4,200,1,3,2]
longestConsecutive(nums)