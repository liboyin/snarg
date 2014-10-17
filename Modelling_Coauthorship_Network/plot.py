from coauthorship_network import new_coauthorship_network
from social_graph_analysis import analyze
import matplotlib.pyplot as pyplot
import pickle


def print_report(name, report):
	print('name={}'.format(name))
	for entry in report:
		print('{}={}'.format(entry, str(report[entry])))


def unzip(pairs):  # TODO replace with @*zip(): https://docs.python.org/3.4/library/functions.html#zip
	xs, ys = [], []
	for (x, y) in pairs:
		xs.append(x)
		ys.append(y)
	return xs, ys


def scatter_plot(entry, title='', x_label='', y_label='', log_scales=False):
	obs_xs, obs_ys = unzip(obs_report[entry].items())
	exp_xs, exp_ys = unzip(exp_report[entry].items())
	pyplot.plot(obs_xs, obs_ys, 'ro', label='observed')
	pyplot.plot(exp_xs, exp_ys, 'b^', label='simulated')
	pyplot.title(title)
	pyplot.xlabel(x_label)
	pyplot.ylabel(y_label)
	pyplot.legend(loc='upper right')
	if log_scales:
		pyplot.xscale('log')
		pyplot.yscale('log')
	pyplot.show()


# obs_name = 'CA-GrQc'
obs_name = 'CA-HepTh'
exp_name = '2014.05.26.21.44.45'
# exp_name = new_coauthorship_network(9877, 51971)
# analyze(exp_name)
postfix = '.analysis_report.pickle'
with open(obs_name + postfix, mode='rb') as file:
	obs_report = pickle.load(file)
with open(exp_name + postfix, mode='rb') as file:
	exp_report = pickle.load(file)
print_report(obs_name, obs_report)
print_report(exp_name, exp_report)
scatter_plot('community_size_distro', title='Community Size Distribution', x_label='Community Size', y_label='Count', log_scales=True)
scatter_plot('degree_distro', title='Vertex Degree Distribution', x_label='Vertex Degree', y_label='Count', log_scales=True)
scatter_plot('hop_distro', title='Hop Distance Cumulative Distribution', x_label='Hop', y_label='Coverage')
scatter_plot('neighbourhood_densities', title='Mean Neighbourhood Density', x_label='Vertex Degree', y_label='Density')
scatter_plot('max_degeneracies', title='Maximum Degeneracy of Neighbourhood', x_label='Vertex Degree', y_label='Degeneracy')