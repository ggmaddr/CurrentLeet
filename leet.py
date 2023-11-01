def productExceptSelf(nums: list[int]) -> list[int]:
    #Create 2 arrays: prefix product and postfix product.
    #Output[i] = prefix[i-1] * postfix [i+1]
    #Time: O(n), Space: O(3n)
    l = len(nums)
    pre, pos= [nums[0]]*l, [nums[l-1]]*l
    j = l - 2
    for i in range(1, l):
        pre[i] = pre[i-1] * nums[i]
        pos[j] = pos[j+1] * nums[j]
        j-=1
    #init first and last in output
    out = [pos[1]]*l
    out[l-1] = pre[l-2]
    
    for i in range(1,l-1):
        out[i] = pre[i-1]*pos[i+1]
    
    print(pre, pos, out)
    return out

nums = [1,2,3,4]
productExceptSelf(nums)