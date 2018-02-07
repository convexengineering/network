from gpkit import Variable, VectorVariable, Model, SignomialsEnabled
from gpkit.constraints.bounded import Bounded
from gpkit.tools import te_exp_minus1
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from math import factorial
from relaxed_constants import relaxed_constants, post_process


class Flow(Model):
    def setup(self,N):
        edgeCost = VectorVariable([N, N],
                                  'edgeCost',edgeCosts)
        edgeMaxFlow = VectorVariable([N, N],
                                     'edgeMaxFlow',edgeMaxFlows)
        flow = VectorVariable([N, N], 'flow')
        source = VectorVariable(N, 'source', sources)
        sink = VectorVariable(N, 'sink', sinks)
        outflow = VectorVariable(N, 'outflow')
        inflow = VectorVariable(N, 'inflow')
        totalCost = Variable('totalCost')

        constraints = []

        with SignomialsEnabled():

            for i in range(0, N):
                constraints.extend([flow[i, i] == 10**-20,
                                    inflow[i] >= source[i] + sum(flow[:, i]),
                                    outflow[i] <= sink[i] + sum(flow[i, :]),
                                    outflow[i] == inflow[i]
                                    ])
                for j in range(0, N):
                    constraints += [flow[i, j] <= edgeMaxFlow[i, j]]

        constraints.extend([totalCost >= sum(edgeCost * flow) +
                            10**7 * sum(outflow) + 10**7 * sum(inflow)])

        return constraints

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
    labelDict = {i: i for i in nodeNames}

    edge_alphas = edge_weights / max(edge_weights)
    nodes = nx.draw_networkx_nodes(g, pos, node_size=900 * abs(node_sizes) / max(abs(node_sizes)),
                                   nodelist=nodeNames, node_color=node_colors, label=nodeNames)
    edges = nx.draw_networkx_edges(g, pos, node_size=900 * abs(node_sizes) / max(abs(node_sizes)),
                                   arrows=True,
                                   width=10 * abs(edge_weights) / max(abs(edge_weights)), edgecolor='b')
    labels = nx.draw_networkx_labels(g, pos, labels=labelDict)
    plt.axis('off')
    plt.show()

    return g


if __name__ == '__main__':

    N = 5
    edgeCosts = [[10000, 140, 100, 80, 80],
                 [140, 10000, 90, 80, 69],
                 [100, 90, 10000, 50, 40],
                 [80, 69, 50, 10000, 70],
                 [90, 100, 80, 50, 10000]]
    edgeMaxFlows =  [[4, 4, 4, 4, 4],
                     [4, 4, 4, 4, 4],
                     [4, 4, 4, 4, 4],
                     [4, 4, 4, 4, 4],
                     [4, 4, 4, 4, 4]]
    sources = [5, 0, 0, 5, 0]
    sinks = [0., 2, 3, 0, 5]

    m = Flow(N)

    m.substitutions.update({
    	'edgeCost':       edgeCosts,
    	'edgeMaxFlow':    edgeMaxFlows,
    	'source'     :    sources,
    	'sink'       :    sinks,
    	})

    m = Model(m.variables_byname('totalCost')[0], Bounded(m))

    # Note: convergence issues in SP solve without relaxed_constants
    m_relax = relaxed_constants(m, None)

    # Solution
    sol = m.localsolve(verbosity=4, reltol=10**-4)
    sol_relax = m_relax.localsolve(verbosity=4, reltol=10**-4)

    # Flow comparison
    flow = np.round(sol('flow'), 5)
    flow_relax = np.round(sol_relax('flow'), 5)

    # Plotting
    g = drawNetwork(sol)
    g = drawNetwork(sol_relax)
