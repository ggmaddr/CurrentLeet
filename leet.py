from collections import defaultdict, deque

def getMinSumNodeValues(service_nodes, service_from, service_to, k, currentValues):
    # Step 1: Construct the graph
    graph = defaultdict(list)
    for i in range(service_nodes - 1):
        graph[service_from[i]].append(service_to[i])
        graph[service_to[i]].append(service_from[i])

    # Step 2: Initialize threads array
    threads = [-1] * service_nodes

    # Step 3: Update known configurations
    for node, value in currentValues:
        threads[node - 1] = value

    # Step 4: BFS traversal to assign ranges
    visited = set()
    queue = deque(currentValues)
    while queue:
        node, value = queue.popleft()
        if node in visited:
            print("GET VISITED")
            continue
        visited.add(node)
        print(node, value)
        for neighbor in graph[node]:
            if isinstance(threads[neighbor-1], int) and threads[neighbor-1] > 0 :
                continue
            
            #if not assigned and next to nint
            if threads[neighbor-1] == -1 and isinstance(value, int):
                threads[neighbor-1] = [value-1, value+1]

            #if neighbor not assigned and next to a range
            elif threads[neighbor-1] == -1 and isinstance(value, list):
                threads[neighbor-1] = [value[0]-1, value[1]+1]
            #if neighbor is an assigned range
            else:
                
                
                
                newmin = min(value[1]+1, threads[neighbor-1][0])
                newmax = max(value[0]-1,threads[neighbor-1][1])
                
                threads[neighbor-1] = [newmin, newmax]
            queue.append((neighbor, threads[neighbor - 1]))
            print(threads)
    
    
            
    
    # Step 5: Return result
    return threads

# Example usage:
service_nodes = 6
service_from = [1, 2, 3, 4,6]
service_to = [2, 3, 4, 5,3]
k = 3
currentValues = [[1, 3], [5, 3], [6, 6]]
print(getMinSumNodeValues(service_nodes, service_from, service_to, k, currentValues))
