
def generateParenthesis(n: int) -> list[str]:
    out = []
    comb = [] #each combination
    #recursion with # of o and c parentheses from 0 to n
    
    def backtrack(ocount, ccount):
        #base case
        if ocount == n and ccount == n:
            out.append("".join(comb))
        
        if ocount < n:
            comb.append('(')
            backtrack(ocount+1, ccount)
            comb.pop()
        if ccount < ocount: 
            comb.append(')')
            backtrack(ocount, ccount+1)
            comb.pop()

    
    backtrack(0,0)
    return out

n = 3
print(generateParenthesis(n))