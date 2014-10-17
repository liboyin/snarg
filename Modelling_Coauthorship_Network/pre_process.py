import os.path as path
import pickle


def read_graph(name):
	if path.isfile(name + '.pickle'):
		with open(name + '.pickle', mode='rb') as file:
			return pickle.load(file)
	edges = set()
	with open(name + '.txt') as file:
		for line in file:
			if line[0] != '#':
				a, b = line.split()
				a, b = int(a), int(b)
				if a != b:
					edges.add((a, b))
	return edges


def extract_vertices(edges):
	vertices = set()
	for (a, b) in edges:
		vertices.add(a)
		vertices.add(b)
	return vertices


def reduce_vertex_id(vertices):
	id_dict = dict()
	index = 0
	for vertex in sorted(list(vertices)):
		id_dict[vertex] = index
		index += 1
	return id_dict