def dailyTemperatures(temperatures: list[int]) -> list[int]:
    
        #Pattern reg: find nearest correlation -> stack.pop get the most recent val within the correlation.
    #Add temps to stacks, only pop when found the nearest warm.
    
    st = [] #val:count stack
    out = [0]*len(temperatures)
    
    for i,t in enumerate(temperatures):
        while st and t > st[-1][0]: #st[-1][0] = temp at top node
            stT,stIndex = st.pop()
            out[stIndex] = i - stIndex            
        st.append((t,i)) #i, t

    return out

# temperatures = [71,71,76,71,71,76,71,71,71,71,76,76,71,71,71,76,76,76,71,76,71,71,71,76,76,76,76,71,71,76,71,76,71,76,71,71,76,76,76,76,71,76,71,71,71,71,71,76,71,76,76,76,76,71,71,71,76,76,71,71,71,71,76,71,71,76,71,71,71,71,76,71,71,71,76,71,76,71,76,76,76,76,76,71,76,71,71,76,71,76,71,76,76,71,71,76,76,76,71,76]
temperatures = [73,74,75,71,69,72,76,73]
print(dailyTemperatures(temperatures))