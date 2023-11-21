def maxRepeating(sequence: str, word: str) -> int:
    i,j = 0, len(word)
    ccount, mxcount = 0,0 #currentcount, maxcount

    while j<=len(sequence):
            temp = sequence[i:j]
            if temp == word:
                ccount +=1
                i += len(word) #on going success
                j += len(word)
            elif temp !=word:
                #reset ccount if ccount > 0
                if ccount > 0:
                    mxcount = max(mxcount, ccount)
                    ccount = 0
                i +=1
                j +=1
    mxcount = max(mxcount, ccount)
    return mxcount
                
    
# Example usage:
short_str = "aaaba"
long_str = "aaabaaaabaaabaaaabaaaabaaaabaaaaba"
result = maxRepeating(long_str, short_str)
print(result)