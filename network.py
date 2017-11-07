from gpkit import Variable, VectorVariable, Model, SignomialsEnabled
from gpkit.constraints.bounded import Bounded
from gpkit.tools import te_exp_minus1
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class basicFlow(Model):
	def setup(N=4):
		edgeCost = VectorVariable([4,4],'edgeCost',[[10000,140,100,80],
									[140, 10000,90, 69],
									[100,90,10000,50],
									[80,69,50,10000]])
		flow = VectorVariable([4,4],'flow')
		source = VectorVariable(4,'source',[10,0,0,0])
		sink = VectorVariable(4,'sink',[0,3,3,4])
		outflow = VectorVariable(4,'outflow')
		inflow = VectorVariable(4,'inflow')
		error = VectorVariable(4,'error')
		totalCost = Variable('totalCost')

		constraints = []

		with SignomialsEnabled():

			for i in range(0,4):
				constraints.extend([flow[i,i] == 10**-10,
					inflow[i] <= source[i] + sum(flow[:,i]),
					outflow[i] >= sink[i] + sum(flow[i,:]),
					outflow[i] == inflow[i]])

		constraints.extend([totalCost >= sum(edgeCost*flow) + 
			 10**5*sum(outflow) + 10**5*sum(inflow)])

		return constraints

if __name__ == '__main__':
	m = basicFlow()
	m = Model(m.variables_byname('totalCost')[0],Bounded(m))
	sol = m.localsolve()

	# Visualize the flow
	g = nx.Graph()
	flow = sol('flow')
	nodeNames = ['a','b','c','d']
	g.add_nodes_from(nodeNames)

	for i in range(0,3):
		for j in range(0,3):
			g.add_edge(nodeNames[i],nodeNames[j],flowRate=flow[i,j])
