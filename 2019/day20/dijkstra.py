
# idea borrowed from https://stackabuse.com/dijkstras-algorithm-in-python/

from queue import PriorityQueue

class Graph:

	def dijkstra(self, start_vertex):
		visited = {}
		D = {start_vertex: (0, None) }

		pq = PriorityQueue()
		pq.put((0, start_vertex))

		while not pq.empty():
			(dist, current_vertex) = pq.get()
			visited[current_vertex] = None

			for neighbor, distance in self.neighbours(current_vertex):
				if neighbor not in visited:
					old_cost = D.get(neighbor, (float('inf'), None))[0]
					new_cost = D[current_vertex][0] + distance
					if new_cost < old_cost:
						pq.put((new_cost, neighbor))
						D[neighbor] = (new_cost, current_vertex)
		return D

	@staticmethod
	def neighbours(current_vertex):
		raise NotImplementedError()

def trace_back(D, start, end):
	ret = []
	current = end
	while current != start:
		ret.append(current)
		current = D[current][1]
	return ret

def next_state(D, start, end):
	current = end
	while D[current][1] != start:
		current = D[current][1]
	return current, D[current][0] - D[start][0]
