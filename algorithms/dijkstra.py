def dijkstra(
    graph: dict[str, dict[str, int | float]], 
    origin: str, 
    destination: str
) -> tuple[list[str], int | float] | None:
    
    costs = {}
    previous = {}
    keys = list(graph.keys())
    
    for node in graph:
        if node == origin:
            costs[node] = 0
        else:
            costs[node] = float('inf')
            
        previous[node] = None
            
    while keys:
        
        best_node = None
        best_cost = float('inf')
        
        for key in keys:
            if costs[key] < best_cost:
                best_cost = costs[key]
                best_node = key
        
        if best_node is None:
            break
        
        if best_node == destination:
            break
                
        for node, distance in graph[best_node].items():
            new_cost = distance + best_cost
            if costs[node] > new_cost:
                costs[node] = new_cost
                previous[node] = best_node
        
        keys.remove(best_node)

    if costs[destination] == float('inf'):
        return None
    
    path = []
    current = destination
    path.append(current)
    while current != origin:
        current = previous[current]
        path.append(current)
    
    path.reverse()
    return path, costs[destination]