from gpkit import Variable, VectorVariable, Model, SignomialsEnabled, SignomialEquality
from gpkit.constraints.bounded import Bounded
from gpkit.tools import te_exp_minus1
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from math import factorial
from relaxed_constants import relaxed_constants, post_process
from drawNetwork import drawNetwork
from MST import MST
from flow import Flow
from flowElems import Node, Edge
from genData import *
from solveNetworkGP import *
from solveNetworkLP import *

if __name__ == '__main__':
    N = 5
    points = np.genfromtxt('6points.csv', delimiter=',')
    pointDict = {str(i): points[i - 1, :] for i in range(1, N + 1)}
    edgeCosts = [[1e-20, 140, 100, 80, 80],
                 [140, 1e-20, 90, 80, 69],
                 [100, 90, 1e-20, 50, 40],
                 [80, 69, 50, 1e-20, 70],
                 [90, 100, 80, 50, 1e-20]]
    edgeMaxFlows = 3. * np.array([[1., 1., 1., 1., 1.],
                                  [1., 1., 1., 1., 1.],
                                  [1., 1., 1., 1., 1.],
                                  [1., 1., 1., 1., 1.],
                                  [1., 1., 1., 1., 1.]])
    sources = [0, 2, 3, 0, 5]
    sinks = [5, 0., 0., 5, 0]
    # sources = [5, 0, 0, 5, 0]
    # sinks = [0., 2, 3, 0, 5]
    # sources = [1, 0, 0, 0, 0]
    # sinks = [0., 0, 0, 0, 1]

    # N = 6
    # points = np.genfromtxt('6points.csv',delimiter=',')
    # pointDict = {str(i):points[i-1,:] for i in range(1,N+1)}
    # edgeCosts = [[0, 140, 100, 80, 80, 70],
    #              [140, 0, 90, 80, 69, 80],
    #              [100, 90, 0, 50, 40, 90],
    #              [80, 69, 50, 0, 70, 60],
    #              [90, 100, 80, 50, 0, 67],
    #              [80, 64, 79, 80, 70, 0]]

    # edgeMaxFlows = [[4, 4, 4, 4, 4, 4],
    #                 [4, 4, 4, 4, 4, 4],
    #                 [4, 4, 4, 4, 4, 4],
    #                 [4, 4, 4, 4, 4, 4],
    #                 [4, 4, 4, 4, 4, 4],
    #                 [4, 4, 4, 4, 4, 4]]
    # sources = [5, 0, 0, 5, 0, 0]
    # sinks = [0, 3, 4, 0, 3, 0]

    # N=5
    # xRange = (-1, 1)
    # yRange = (-1, 1)
    # genData(xRange,yRange,N)

    # points = np.genfromtxt('points.csv',delimiter=',')
    # pointDict = {str(i):points[i-1,:] for i in range(1,N+1)}

    # eucDist    = np.genfromtxt('eucDist.csv',delimiter=',')
    # edgeCosts  = np.genfromtxt('edgeCosts.csv',delimiter=',')
    # edgeMaxFlows = np.ones((N,N)) * N
    # sources = np.genfromtxt('sources.csv',delimiter=',')
    # sinks = np.genfromtxt('sinks.csv',delimiter=',')

    #     sources      = np.zeros(N)
    #     sources[0]   = N-1
    #     sinks        = np.zeros(N)
    #     sinks[1:]    = 1.

    # GP and LP Solutions

    m = Flow(N)
    m.substitutions.update({
        'edgeCost': edgeCosts,
        'edgeMaxFlow': edgeMaxFlows,
        'source': sources,
        'sink': sinks,
    })
    m.substitutions.update({'slackCost': 50})  # ['sweep',np.linspace(100,10000,10)]})
    m.cost = np.sum(m['edgeCost'] * m['flow'])*(1 + m['slackCost']*np.prod(m['slackOne'])*np.prod(m['slackTwo']))  # + 10000*np.prod(m['slackOne']) + 10000*np.prod(m['slackTwo'])
    # m = relaxed_constants(m)
    solGP = m.localsolve(verbosity=3, reltol=1e-7, iteration_limit=100, pccp_penalty=5)
    solLP = solveNetworkLP(N, edgeCosts, edgeMaxFlows, sources, sinks)

    # solGP = solveNetworkGP(N,edgeCosts,edgeMaxFlows,sources,sinks)
    # solLP = solveNetworkLP(N,edgeCosts,edgeMaxFlows,sources,sinks)

    # Flow comparison
    # flowGP = np.round(solGP('flow'), 3)
    # connectivityGP = np.round(solGP('connectivity'), 3)
    # flowLP = np.round(solLP['flow'], 3)
    # connectivityLP =

    # Plotting
    g = drawNetwork(solGP, points=pointDict)
    plt.figure()
    g = drawNetwork(solLP, points=pointDict)

    # Printing relative costs and slack
    # print 'Flow Cost: ' + str(np.round(sum(sum(solGP('edgeCost') * solGP('flow'))), 3))
    # print 'Slack Cost: ' + str(solGP('slackCost') * np.prod(solGP('slack')))
    # print 'Slack: ' + str(solGP('slack'))
    # print 'Connectivity: ' + str(np.round(solGP('connectivity'), 3))
