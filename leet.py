from collections import defaultdict
def countPairs(arr: list[int], n: int) -> int:
    # Initialize answer and maximum value in the array
    ans, mx = 0, 0
    # Create a defaultdict to store the frequency of each integer in the array
    mp = defaultdict(int)
    # Iterate through each integer in the array
    for ai in arr:
        # Update the frequency of each integer in the defaultdict
        mp[ai] += 1
        # Update the maximum value in the array
        mx = max(mx, ai)
    # Iterate through each integer i from 0 to mx
    for i in range(mx+1):
        # If i is not present in the defaultdict, skip to the next integer
        if i not in mp:
            continue
        # Iterate through each integer j from i to mx
        for j in range(i, mx+1):
            # If j is not present in the defaultdict, skip to the next integer
            if j not in mp:
                continue
            # Check if the bitwise AND of i and j has only one set bit
            if bin(i & j).count('1') == 1:
                # If i is equal to j, add the product of nCr(mp.get(i), 2) 
                # to the answer
                if i == j:
                    ans += (mp[i] * (mp[i]-1)) // 2
                # If i is not equal to j, add the product of mp.get(i) 
                # and mp.get(j) to the answer
                else:
                    ans += mp[i] * mp[j]
    # Return the answer
    return ans
arr = [6, 4, 2, 3]
n = len(arr)
print(countPairs(arr, n))