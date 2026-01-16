from collections import Counter, defaultdict
def get_minimum_window(original: str, check: str) -> str:
    visited = defaultdict(int) #visited {char: count}; if use defaultdict, notice to not check eq with checkmap[i] for value = 0
    match = 0 #counts of chars match
    checkmap = Counter(check)
    res, resLen = [-1, -1], float('inf')
    l = 0
    for r in range(len(original)):
        visited[original[r]] += 1
        if visited[original[r]] == checkmap[original[r]] and visited[original[r]]!=0: 
            match += 1
           
        # shrink after found a candidate to be ready for new candidate:
        while match == len(checkmap):
             # if match character and smaller len, update result
            if r-l+1 < resLen or (r-l+1 == resLen and original[l:r+1] < original[res[0]: res[1] + 1]):
                res = [l, r]
                resLen = r-l+1
            #shrink
            visited[original[l]] -= 1
            if visited[original[l]] < checkmap[original[l]]:
                match-=1
            l += 1
    return original[res[0]: res[1] + 1] if res != [-1, -1] else ""

original = "cdbaeeebaecd"
check = "abc"
print(get_minimum_window(original, check)   )