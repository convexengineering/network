from gpkit import solution_array as sa
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def drawNetwork(sol, points=[]):
    # Visualize the flow
    g = nx.DiGraph()
    if type(sol) is sa.SolutionArray:
        flow = np.round(sol('flow'), 3)
    elif type(sol) is dict:
        flow = np.round(sol['flow'], 3)
    else:
        raise TypeError(f"Solution of type {type(sol)} is invalid.")

    Nnodes = len(flow)
    sources = np.round([sum(flow[i, :]) - sum(flow[:, i])
                        for i in range(Nnodes)], 3)

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

    if points == []:
        pos = nx.shell_layout(g)
    else:
        pos = points

    node_sizes = sources

    node_colors = ['r' if i < 0 else 'b' for i in node_sizes]
    nodeLabelDict = nx.get_node_attributes(g, 'weight')
    edgeLabelDict = nx.get_edge_attributes(g, 'weight')

    # Deleting zero entries from edges
    for i in list(edgeLabelDict.keys()):
        if edgeLabelDict[i] == 0:
            edgeLabelDict.pop(i)

    edgeVals = np.array(list(edgeLabelDict.values()))

    edge_alphas = edge_weights / max(edge_weights)
    nodes = nx.draw_networkx_nodes(g, pos, node_size=900 * abs(node_sizes) / max(abs(node_sizes)),
                                   nodelist=nodeNames, node_color=node_colors, label=nodeLabelDict)
    edges = nx.draw_networkx_edges(g, pos, node_size=900 * abs(node_sizes) / max(abs(node_sizes)),
                                   edgelist=list(edgeLabelDict.keys()), arrows=True,
                                   width=10 * abs(edgeVals) / max(abs(edgeVals)), edge_color='b')
    nodeLabels = nx.draw_networkx_labels(g, pos, labels=nodeLabelDict, font_size=16)
    edgeLabels = nx.draw_networkx_edge_labels(g, pos, label_pos=0.2,
                                              edge_labels=edgeLabelDict, font_size=14, font_color='m')
    plt.axis('off')
    plt.show()

    return g
