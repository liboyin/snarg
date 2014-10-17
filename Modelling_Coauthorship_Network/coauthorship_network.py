from math import e
from time import gmtime, strftime, time
import random


class CoauthorshipNetwork:
	def __init__(self, researcher_count, coauthorship_count):
		self.researcher_count, self.coauthorship_count = researcher_count, coauthorship_count
		self.coauthorships = [dict() for _ in range(0, self.researcher_count)]  # researcher -> coauthor -> paper count
		self.author_pairs = set()  # (i, j), where i < j, represents a coauthor relationship

	def fitness(self, researcher, base=1):
		experience = sum(self.coauthorships[researcher].values())  # summation of the number of papers across coauthors
		age = e ** (experience / 20) - 1  # @age overruns @experience at around 40
		return max(0, base + experience - age)

	def neighbour_degrees(self, selected):
		neighbours = dict()
		for researcher in selected:
			for past_coauthor in self.coauthorships[researcher].keys():
				if past_coauthor not in selected:
					if past_coauthor not in neighbours:
						neighbours[past_coauthor] = 0
					neighbours[past_coauthor] += 1
		return neighbours

	def register(self, selected):
		for i in selected:
			for j in selected:
				if j not in self.coauthorships[i]:
					self.coauthorships[i][j] = 0
				self.coauthorships[i][j] += 1
				if i < j:
					self.author_pairs.add((i, j))

	def run(self):
		initial_coverage = set(range(0, self.researcher_count))  # ensures that every researcher has written at least one paper
		old_percentage = -1
		while len(self.author_pairs) < self.coauthorship_count:
			new_percentage = int(len(self.author_pairs)/self.coauthorship_count*100)
			if new_percentage > old_percentage:
				print('{}%'.format(new_percentage))
				old_percentage = new_percentage
			group_size = int(abs(random.gauss(mu=0, sigma=2))+2)  # RHS of normal distribution (mu=2, sigma=2)
			if len(initial_coverage) > 0:
				selected = set(initial_coverage.pop() for _ in range(0, group_size) if len(initial_coverage) > 0)  # select with uniform distribution
			else:
				selected = set()
				selected.add(self.roulette_wheel(range(0, self.researcher_count), self.fitness))  # add seed, then expand greedily
				while len(selected) < group_size:
					neighbours = self.neighbour_degrees(selected)  # neighbours of @selected -> friend count in @selected
					if len(neighbours) == 0 or random.random() < 0.05:
						selected.add(self.roulette_wheel(range(0, self.researcher_count), self.fitness))  # from all researchers
					else:
						selected.add(self.roulette_wheel(list(neighbours.keys()), lambda x: self.fitness(x, neighbours[x]*100)))  # from @neighbours, with friend count emphasized
			self.register(selected)
		return self.author_pairs

	@staticmethod
	def roulette_wheel(xs, fit_fun):
		fitness = [fit_fun(x) for x in xs]
		key = random.random() * sum(fitness)
		for i in range(0, len(xs)):
			if key <= 0:
				return xs[i]
			key -= fitness[i]
		return xs[0]


def new_coauthorship_network(researcher_count, coauthorship_count):
	name = strftime('%Y.%m.%d.%H.%M.%S', gmtime())
	print('name={}'.format(name))
	print('researcher_count={}, coauthorship_count={}'.format(researcher_count, coauthorship_count))
	start_time = time()
	author_pairs = CoauthorshipNetwork(researcher_count, coauthorship_count).run()
	with open(name + '.txt', mode='w') as file:
		file.write('# vertices: {}, edges: {}\n'.format(researcher_count, coauthorship_count))
		for (a, b) in author_pairs:
			file.write('{}\t{}\n'.format(a, b))
	print('100%\nelapsed_time={}s'.format(time()-start_time))
	return name