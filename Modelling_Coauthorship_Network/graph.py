import numpy


class Graph(dict):
	def __init__(self, edges):  # @author_pairs must have reduced id
		super().__init__()
		for (a, b) in edges:
			if a != b:
				self.add_edge(a, b)
				self.add_edge(b, a)

	def add_edge(self, a, b):
		if a not in self:
			self[a] = set()
		self[a].add(b)

	def to_matrix(self):
		size = len(self)
		matrix = numpy.zeros((size, size), dtype=numpy.int)
		for a in self:
			for b in self[a]:
				matrix[a, b] = 1
		return matrix

	def bin_vertices_by_degree(self):
		bins = dict()
		for vertex in self:
			degree = len(self[vertex])
			if degree not in bins:
				bins[degree] = set()
			bins[degree].add(vertex)
		return bins

	def neighbourhood_subgraph(self, vertex):
		edges = set()
		for a in self[vertex]:
			for b in self[vertex]:
				if a < b and b in self[a]:
					edges.add((a, b))
		return Graph(edges)