def twoSum(numbers: list[int], target: int) -> list[int]:
    #2 pointers: at start and at end. 
    # When sum(nums[i]+nums[j])> target -> decrement end p (decrease larger num in the sum)
    #sum(nums[i]+nums[j]) < target -> increase start p 
    #Time: O(n), Space: O(1)
    
    pre, pos = 0, len(numbers)-1
    while pre < pos:
        sum = numbers[pre]+numbers[pos]
        if sum < target:
            pre += 1
        elif sum > target:
            pos -= 1
        else:
            return [pre+1, pos+1]
    return []
numbers = [2,7,11,15]
target = 9
print(twoSum(numbers, target))