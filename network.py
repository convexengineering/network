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
from flowElems import Node,Edge
from genData import *

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
    xRange = (-1, 1)
    yRange = (-1, 1)
    genData(xRange,yRange,N)
    points = np.genfromtxt('points.csv',delimiter=',')
    pointDict = {str(i):points[i-1,:] for i in range(1,N+1)}
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
    #connect = np.ones([6,6]) 
    sources = [5, 0, 0, 5, 0, 0]
    sinks = [0, 3, 4, 0, 3, 0]


#     N=6
#     xRange = (-1, 1)
#     yRange = (-1, 1)
#     genData(xRange,yRange,N)

#     points = np.genfromtxt('points.csv',delimiter=',')
#     pointDict = {str(i):points[i-1,:] for i in range(1,N+1)}

#     eucDist    = np.genfromtxt('eucDist.csv',delimiter=',')
#     edgeCosts  = np.genfromtxt('edgeCosts.csv',delimiter=',')
#     edgeMaxFlows = np.ones((N,N)) * N
# #    connect      = np.ones((N,N))
#     sources = np.genfromtxt('sources.csv',delimiter=',')
#     sinks = np.genfromtxt('sinks.csv',delimiter=',')

#     sources      = np.zeros(N)
#     sources[0]   = N-1
#     sinks        = np.zeros(N)
#     sinks[1:]    = 1.

    m = Flow(N)

    m.substitutions.update({
    	'edgeCost':       edgeCosts,
    	'edgeMaxFlow':    edgeMaxFlows,
    #	'connectivity':   connect,
    	'source'     :    sources,
    	'sink'       :    sinks,
    	})

    m = Model(m.variables_byname('totalCost')[0], Bounded(m))

    # Note: potential convergence issues with or without relaxed_constants. 
    #m = relaxed_constants(m, None)

    # Solution
    sol = m.localsolve(verbosity=4, reltol=10**-4,iteration_limit=100)

    # Flow comparison
    flow = np.round(sol('flow'), 3)
    connectivity = np.round(sol('connectivity'), 3)


    # Plotting
    g = drawNetwork(sol, points = pointDict)

