class UnionFind:
	def __init__(self, size):
		self.pointers = [i for i in range(0, size)]

	def ancestor(self, i):
		if self.pointers[i] == i:
			return i
		else:
			root = self.ancestor(self.pointers[i])
			self.pointers[i] = root
			return root

	def query(self, a, b):
		return self.ancestor(a) == self.ancestor(b)

	def union(self, a, b):
		self.pointers[self.ancestor(a)] = self.ancestor(b)

	def compress(self):
		for i in range(0, len(self.pointers)):
			self.pointers[i] = self.ancestor(i)

	def get_trees(self):
		self.compress()
		trees = dict()
		for i in range(0, len(self.pointers)):
			root = self.pointers[i]
			if root not in trees:
				trees[root] = set()
			trees[root].add(i)
		return trees