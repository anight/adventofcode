
# idea borrowed from https://stackabuse.com/dijkstras-algorithm-in-python/

from queue import PriorityQueue

class Graph:
    def __init__(self, num_of_vertices, get_neighbours):
        self.v = num_of_vertices
        self.get_neighbours = get_neighbours
        self.visited = {}

def dijkstra(graph, start_vertex):
    D = {v:float('inf') for v in range(graph.v)}
    D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited[current_vertex] = None

        for neighbor, distance in graph.get_neighbours(current_vertex):
            if neighbor not in graph.visited:
                old_cost = D[neighbor]
                new_cost = D[current_vertex] + distance
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    D[neighbor] = new_cost
    return D

