def productExceptSelf(nums: list[int]) -> list[int]:
        #Create an preArr stores prefix product up to + (exclude) nums[i]
        #Loop from the end of preArr: at each preArr[i], multiply by current postfix product var

        #Time: O(n), Space: O(n)
        l = len(nums)
        out = [1] * l
        
        for i in range(1, l):
            #Create an preArr stores prefix product up to nums[i] + (exclude) nums[i]
            out[i] = out[i-1] * nums[i-1]
        print(out)
        #init first and last in output
        pos = nums[l-1]
        for i in range(l-2, -1, -1):
            out[i] = out[i] * pos  #upto prefix * upto postfix 
            pos *= nums[i]
        
        print(out)
        return out
nums = [1,2,3,4]
print(productExceptSelf(nums))
