from graph import Graph
from numpy import mean
from pre_process import *
from scipy.sparse.csgraph import floyd_warshall
from time import time
from union_find import UnionFind
import os.path as path
import pickle


def lazy_transitive_matrix(graph, name):
	filename = name + '.transitive_matrix.pickle'
	if path.isfile(filename):
		with open(filename, mode='rb') as file:
			return pickle.load(file)
	matrix = floyd_warshall(graph.to_matrix(), directed=False)
	with open(filename, mode='wb') as file:
		pickle.dump(matrix, file)
	return matrix


def community_size_distribution(vertices, edges):  # @author_pairs and @vertices must have reduced id
	communities = UnionFind(len(vertices))
	for (a, b) in edges:
		communities.union(a, b)
	trees = communities.get_trees()
	distro = dict()
	for tree in trees:
		size = len(trees[tree])
		if size not in distro:
			distro[size] = 0
		distro[size] += 1
	return distro


def hop_cumulative_distribution(matrix):  # @matrix must be transitive numpy array
	distro = dict()
	for i in range(0, len(matrix)):
		for j in range(0, i):  # each pair is counted only once
			hop = matrix[i, j]
			if 0 < hop < float('Inf'):
				hop = int(hop)
				if hop not in distro:
					distro[hop] = 0
				distro[hop] += 1
	sorted_distro = list(sorted(distro.items(), key=lambda x: x[0]))
	acc = 0
	for (hop, count) in sorted_distro:
		acc += count
		distro[hop] = acc
	for hop in distro:
		distro[hop] /= acc
	return distro


def neighbourhood_density(vertex, graph):
	n = len(graph[vertex])
	if n < 2:  # causes divide by zero exception
		return 1
	count = 0
	for a in graph[vertex]:
		for b in graph[vertex]:
			if a < b and a in graph[b]:  # each edge is counted only once
				count += 1
	return (count*2)/(n*(n-1))


def degeneracy(vertex, graph):
	neighbourhood = graph.neighbourhood_subgraph(vertex)
	if len(neighbourhood) == 0:
		return 0
	lonely_neighbour = min(neighbourhood, key=lambda x: len(neighbourhood[x]))
	max_min_degree = len(neighbourhood[lonely_neighbour])
	while True:
		del neighbourhood[lonely_neighbour]
		if len(neighbourhood) == 0:
			break
		for neighbour in neighbourhood:
			neighbourhood[neighbour].discard(lonely_neighbour)
		lonely_neighbour = min(neighbourhood, key=lambda x: len(neighbourhood[x]))
		max_min_degree = max(max_min_degree, len(neighbourhood[lonely_neighbour]))
	return max_min_degree


def analyze(name='CA-GrQc'):
	print('name={}'.format(name))
	start_time = time()
	raw_edges = read_graph(name)
	raw_vertices = extract_vertices(raw_edges)
	id_dict = reduce_vertex_id(raw_vertices)
	reduced_edges = set((id_dict[a], id_dict[b]) for (a, b) in raw_edges)
	reduced_vertices = set(id_dict[vertex] for vertex in raw_vertices)
	print('pre-processing done')
	community_size_distro = community_size_distribution(reduced_vertices, reduced_edges)
	print('community_size_distribution done')
	graph = Graph(reduced_edges)
	bins_by_degree = graph.bin_vertices_by_degree()
	print('graph construction done')
	degree_distro = dict((degree, len(bins_by_degree[degree])) for degree in bins_by_degree)
	print('degree_distribution done')
	hop_distro = hop_cumulative_distribution(lazy_transitive_matrix(graph, name))
	print('hop_cumulative_distribution done')
	neighbourhood_densities = dict((degree, mean([neighbourhood_density(vertex, graph) for vertex in bins_by_degree[degree]])) for degree in bins_by_degree)
	print('neighbourhood_densities done')
	max_degeneracies = dict((degree, max(degeneracy(vertex, graph) for vertex in bins_by_degree[degree])) for degree in bins_by_degree)
	print('max_degeneracies done')
	analysis_report = dict([('community_size_distro', community_size_distro),
							('degree_distro', degree_distro),
							('hop_distro', hop_distro),
							('neighbourhood_densities', neighbourhood_densities),
							('max_degeneracies', max_degeneracies)])
	with open(name + '.analysis_report.pickle', mode='wb') as file:
		pickle.dump(analysis_report, file)
	print('elapsed_time={}s'.format(time()-start_time))