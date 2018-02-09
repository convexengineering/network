from gpkit import Variable, VectorVariable, Model, SignomialsEnabled
from gpkit.constraints.bounded import Bounded
from gpkit.tools import te_exp_minus1
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from math import factorial
from relaxed_constants import relaxed_constants, post_process

class Flow(Model):
    def setup(self, N):
        edgeCost = VectorVariable([N, N],
                                  'edgeCost')
        edgeMaxFlow = VectorVariable([N, N],
                                     'edgeMaxFlow')
        flow = VectorVariable([N, N], 'flow')
        source = VectorVariable(N, 'source')
        sink = VectorVariable(N, 'sink')
        totalCost = Variable('totalCost')

        constraints = []

        with SignomialsEnabled():

            for i in range(0, N):
                constraints.extend([sink[i] + sum(flow[i, :]) >= source[i] + sum(flow[:, i])])
                for j in range(0, N):
                    constraints += [flow[i, j] <= edgeMaxFlow[i, j]]
            for i in range(0, N):
                for j in range(i + 1, N):
                    constraints.extend([flow[i, j] * flow[j, i] <= 1e-5])
        constraints.extend([totalCost >= sum(edgeCost * flow)])
        return constraints

class Node(Model):
	def setup(self,linkedEdges):
		source = Variable()
		sink = Variable()

class Edge(Model):
	def setup(self,inNode,outNode):
		edgeFlow = Variable('edgeFlow')

def drawNetwork(sol):
    # Visualize the flow
    g = nx.DiGraph()
    flow = np.round(sol('flow'), 5)
    Nnodes = len(flow)
    sources = np.round([sum(flow[i, :]) - sum(flow[:, i])
                        for i in range(Nnodes)], 5)

    Nedges = int((1 + (Nnodes - 1)) * (Nnodes - 1) * .5)
    nodeNames = [str(i) for i in range(1, Nnodes + 1)]
    g.add_nodes_from(nodeNames)

    edge_alphas = np.zeros(Nedges)
    edge_weights = np.zeros(Nedges)

    count = 0
    for i in range(0, Nnodes):
        for j in range(0, Nnodes):
            if j > i:
                edge_weights[count] = flow[i, j] - flow[j, i]
                if edge_weights[count] > 0:
                    g.add_edge(nodeNames[i], nodeNames[j],
                               weight=abs(edge_weights[count]))
                else:
                    g.add_edge(nodeNames[j], nodeNames[i],
                               weight=abs(edge_weights[count]))
                count += 1

    pos = nx.shell_layout(g)

    node_sizes = sources

    node_colors = ['r' if i < 0 else 'b' for i in node_sizes]
    nodeLabelDict = nx.get_node_attributes(g,'weight')
    edgeLabelDict = nx.get_edge_attributes(g,'weight')

    # Deleting zero entries from edges
    for i in edgeLabelDict.keys():
    	if edgeLabelDict[i] == 0:
    		edgeLabelDict.pop(i)

    edgeVals = np.array(edgeLabelDict.values())

    edge_alphas = edge_weights / max(edge_weights)
    nodes = nx.draw_networkx_nodes(g, pos, node_size=900 * abs(node_sizes) / max(abs(node_sizes)),
                                   nodelist=nodeNames, node_color=node_colors, label=nodeLabelDict)
    edges = nx.draw_networkx_edges(g, pos, node_size=900 * abs(node_sizes) / max(abs(node_sizes)),
                                   edgelist = edgeLabelDict.keys(),arrows=True,
                                   width=10 * abs(edgeVals) / max(abs(edgeVals)), edgecolor='b')
    nodeLabels = nx.draw_networkx_labels(g, pos, labels=nodeLabelDict,font_size=16)
    edgeLabels = nx.draw_networkx_edge_labels(g, pos, label_pos=0.2, 
    								edge_labels=edgeLabelDict, font_size=14, font_color='m')
    plt.axis('off')
    plt.show()

    return g


if __name__ == '__main__':

    # N = 5
    # edgeCosts = [[0, 140, 100, 80, 80],
    #              [140, 0, 90, 80, 69],
    #              [100, 90, 0, 50, 40],
    #              [80, 69, 50, 0, 70],
    #              [90, 100, 80, 50, 0]]
    # edgeMaxFlows =  [[4, 4, 4, 4, 4],
    #                  [4, 4, 4, 4, 4],
    #                  [4, 4, 4, 4, 4],
    #                  [4, 4, 4, 4, 4],
    #                  [4, 4, 4, 4, 4]]
    # sources = [5, 0, 0, 5, 0]
    # sinks = [0., 2, 3, 0, 5]

    N = 6
    edgeCosts = [[0, 140, 100, 80, 80, 70],
                 [140, 0, 90, 80, 69, 80],
                 [100, 90, 0, 50, 40, 90],
                 [80, 69, 50, 0, 70, 60],
                 [90, 100, 80, 50, 0, 67],
                 [80, 64, 79, 80, 70, 0]]

    edgeMaxFlows = [[4, 4, 4, 4, 4, 4],
                    [4, 4, 4, 4, 4, 4],
                    [4, 4, 4, 4, 4, 4],
                    [4, 4, 4, 4, 4, 4],
                    [4, 4, 4, 4, 4, 4],
                    [4, 4, 4, 4, 4, 4]]
    sources = [5, 0, 0, 5, 0, 0]
    sinks = [0, 3, 4, 0, 3, 0]

    m = Flow(N)

    m.substitutions.update({
    	'edgeCost':       edgeCosts,
    	'edgeMaxFlow':    edgeMaxFlows,
    	'source'     :    sources,
    	'sink'       :    sinks,
    	})

    m = Model(m.variables_byname('totalCost')[0], Bounded(m))

    # Note: potential convergence issues with or without relaxed_constants. 
    #m = relaxed_constants(m, None)

    # Solution
    sol = m.localsolve(verbosity=4, reltol=10**-4,iteration_limit=100)

    # Flow comparison
    flow = np.round(sol('flow'), 5)

    # Plotting
    g = drawNetwork(sol)
