# def longest_palindromic_substring(s):
#     # preprocess the string to insert '#' between characters
#     # and '^' at the start and '$' at the end to simplify boundaries.
#     t = "^#" + "#".join(s) + "#$"
#     n = len(t)
#     p = [0] * n  # Array to store the length of the palindrome radius
#     C = 0  # Center of the current palindrome
#     R = 0  # Right boundary of the current palindrome
#     mmax = 0
#     mword = ""
#     for i in range(1, n - 1):
#         # Mirror of the current position `i` with respect to center `C`
#         mirror = 2 * C - i

#         # Use previously computed palindrome length if within boundary
#         #limit p[i] to R - i, we ensure that: palindrome at i within boundary. Further expansion will only happen if the characters beyond R match symmetrically around i, which will be handled by the while loop that follows.
#         if i < R:
#             p[i] = min(R - i, p[mirror]) #If i too close to bound R, pal might get "cut off" by R

#         # Expand around center `i`
#         a,b = t[i + p[i] + 1], t[i - p[i] - 1]
#         while t[i + p[i] + 1] == t[i - p[i] - 1]:
#             p[i] += 1
       
            
#         # Update center and right boundary
#         if i + p[i] > R:
#             C, R = i, i + p[i]
            
#         if p[i] > mmax:
#             mmax = p[i]
#             mword = t[p[i]-(R-p[i]:p[i])]+t[p[i]:R]

#     # Find the longest palindrome considering lexicographical order
#     max_len = 0
#     start_index = 0
#     for i in range(1, n - 1):
#         if p[i] > max_len:
#             max_len = p[i]
#             start_index = (i - max_len) // 2
#         elif p[i] == max_len:  # If lengths are equal, check lexicographical order
#             temp = (i - max_len) // 2
#             if s[temp:temp + max_len] < s[start_index:start_index + max_len]:
#                 start_index = temp

#     return s[start_index:start_index + max_len]

# # s = "abacdfgdcabba"
# s = "baabaab"

# print(longest_palindromic_substring(s))  # Output: "abba"



def leftmostBuildingQueries(heights, queries):
    mono_stack = []
    result = [-1 for _ in range(len(queries))]
    new_queries = [[] for _ in range(len(heights))]
    for i in range(len(queries)):
        a = queries[i][0]
        b = queries[i][1]
        if a > b:
            a, b = b, a
        if heights[b] > heights[a] or a == b:
            result[i] = b
        else:
            new_queries[b].append((heights[a], i))
    print(new_queries)
    for i in range(len(heights) - 1, -1, -1):
        mono_stack_size = len(mono_stack)
        for a, b in new_queries[i]:
            print("@@AT height", i, "query", b)
            position = search(a, mono_stack)
            if position >= mono_stack_size:
                print("&&&pos < len happens with")
            if position >= 0:
                result[b] = mono_stack[position][1]
            
        while mono_stack and mono_stack[-1][0] <= heights[i]:
            print("idx pop top", i, mono_stack[-1][0])
            mono_stack.pop()
        mono_stack.append((heights[i], i))
    return result

def search(height, mono_stack):
    left = 0
    right = len(mono_stack) - 1
    ans = -1
    while left <= right:
        
        mid = (left + right) // 2
        print("mid idx-val - height is ", mid, mono_stack[mid][0], height )
        if mono_stack[mid][0] > height:
            ans = max(ans, mid)
            left = mid + 1
        else:
            right = mid - 1
    return ans
heights = [5,3,8,2,3,5,2,4,6,5,5,7]
queries = [(0,3), (5,6), (8,10), (0,6), (7,2), (6,1), (1,5), (0,7), (3,5)]
print(leftmostBuildingQueries( heights, queries))
    
    