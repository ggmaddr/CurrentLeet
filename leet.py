def isValid(s: str) -> bool:
    brack = {'{':'}', '[':']', '(':')'}
    stack = []
    for i in range(len(s)):
        if s[i] in brack.keys():
            stack.append(s[i])
        elif len(stack) != 0:
            if s[i] != brack[stack[-1]]: #peek
                return False
            stack.pop()
        # len(stack) == 0 + still have non-open char -> illegal close char
        elif len(stack) == 0: 
            return False
    if len(stack) != 0:
        return False
    return True


s = "{[]}"
print(isValid(s))