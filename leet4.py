def dailyTemperatures(temperatures: list[int]) -> list[int]:
    
    #Pattern reg: find nearest correlation -> stack.pop get the most recent val within the correlation.

    st = [] #arrays of tuple (temp:index)
    out = [0]*len(temperatures)
    #Add temps to stack maintaining decreasingly monotonic, 
    for i,t in enumerate(temperatures):
        #only (keep) pop when found the nearest warm (increase t)
        while st and t > st[-1][0]: #st[-1][0] = top stack temp
            stTemp,stIndex = st.pop()
            out[stIndex] = i - stIndex            
        st.append((t,i)) #i, t

    return out

print(dailyTemperatures([73,74,75,71,69,72,76,73]))