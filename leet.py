def threeSum(nums: list[int]) -> list[list[int]]:
    print("TEST RESULT: -------------------------------------")
    nums.sort()
    res = []
    print(nums)
    i, k, j = 0, 1, len(nums)-1
    while k < j:
        if nums[i]+nums[k]+nums[j] == 0:
            return [[nums[i],nums[k],nums[j]]]     
             
        while nums[i] + nums[j] + nums[j] <= 0:
            i+=1
            if i == len(nums):
                return res
        
        k = i+1
        print(i, k, j)
        if nums[i]+nums[j]+nums[k] == 0:
            res.append([nums[i],nums[k],nums[j]])
            if
            j-=1
            i+=1
        else:
            if nums[i]+nums[j]+nums[k] < 0:
                i+=1
            else:
                j-=1
    return res
nums = [-1,0,1,2,-1,-4]

nums1= [-2,0,1,1,2]
display(threeSum(nums1))
display(threeSum(nums2))