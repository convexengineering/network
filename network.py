from gpkit import Variable, VectorVariable, Model, SignomialsEnabled
from gpkit.constraints.bounded import Bounded
from gpkit.tools import te_exp_minus1
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from math import factorial


class basicFlow(Model):
	def setup(N=4):
		edgeCost = VectorVariable([5,5],
			'edgeCost',[[10000,140,100,80,80],
						[140, 10000,90, 80, 69],
						[100,90,10000,50,40],
						[80,69,50,10000,70],
						[90,100,80,50,10000]])
		edgeMaxFlow = VectorVariable([5,5],
			'edgeMaxFlow',[[4,4,4,4,4],
						   [4,4,4,4,4],
						   [4,4,4,4,4],
						   [4,4,4,4,4],
						   [4,4,4,4,4]])
		flow = VectorVariable([5,5],'flow')
		source = VectorVariable(5,'source',[5,0,0,5,0])
		sink = VectorVariable(5,'sink',[0.,2,3,0,5])
		outflow = VectorVariable(5,'outflow')
		inflow = VectorVariable(5,'inflow')
		totalCost = Variable('totalCost')

		constraints = []

		with SignomialsEnabled():

			for i in range(0,5):
				constraints.extend([flow[i,i] == 10**-20,
					inflow[i] >= source[i] + sum(flow[:,i]),
					outflow[i] <= sink[i] + sum(flow[i,:]),
					outflow[i] == inflow[i]
					])
				for j in range(0,5):
					constraints += [flow[i,j] <= edgeMaxFlow[i,j]]

		constraints.extend([totalCost >= sum(edgeCost*flow) + 
			 10**7*sum(outflow) + 10**7*sum(inflow)])

		return constraints

class Node(Model):
	def setup(self,edgeList):
		flow = VectorVariable('')

def drawNetwork(sol):
	#Visualize the flow
	g = nx.Graph()
	flow = sol('flow')
	sources = sol('source')
	sinks = sol('sink')
	nodeNames = ['a','b','c','d','e']
	g.add_nodes_from(nodeNames)



if __name__ == '__main__':
	m = basicFlow()
	m = Model(m.variables_byname('totalCost')[0],Bounded(m))
	sol = m.localsolve(verbosity=4)

	g = nx.Graph()
	flow = sol('flow')
	sources = sol('source')
	sinks = sol('sink')
	nodeNames = ['a','b','c','d','e']
	g.add_nodes_from(nodeNames)


	edge_alphas = np.zeros(10)
	edge_weights = np.zeros(10)

	count = 0
	for i in range(0,5):
		for j in range(0,5):
			if j > i:
				edge_weights[count] = flow[i,j]-flow[j,i]
				if edge_weights[count] > 0:
					g.add_edge(nodeNames[i],nodeNames[j],weight=abs(edge_weights[count]))
				else:
					g.add_edge(nodeNames[j],nodeNames[i],weight=abs(edge_weights[count]))
				count += 1

	pos = nx.shell_layout(g)

	node_sizes = sources - sinks
	node_colors = ['r' if i < 0 else 'b' for i in node_sizes]

	edge_alphas = edge_weights/max(edge_weights)
	nodes = nx.draw_networkx_nodes(g,pos,nodesize=abs(node_sizes),nodelist=nodeNames,node_color=node_colors)
	edges = nx.draw_networkx_edges(g, pos,nodesize=abs(node_sizes),arrowstyle='->',arrowsize=10,width=abs(edge_weights),edgecolor='b')

	m = g.number_of_edges()

	plt.axis('off')
	plt.show()

	# Example code
# 	G = nx.generators.directed.random_k_out_graph(10, 3, 0.5)
# pos = nx.layout.spring_layout(G)

# node_sizes = [3 + 10 * i for i in range(len(G))]
# M = G.number_of_edges()
# edge_colors = range(2, M + 2)
# edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

# nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
# edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
#                                arrowsize=10, edge_color=edge_colors,
#                                edge_cmap=plt.cm.Blues, width=2)
# # set alpha value for each edge
# for i in range(M):
#     edges[i].set_alpha(edge_alphas[i])

# ax = plt.gca()
# ax.set_axis_off()
# plt.show()