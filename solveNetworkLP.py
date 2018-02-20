import scipy
import numpy as np

def flatten(A):
    flat_list = []
    for sublist in A:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def square(vec):
    N = int(len(vec)**0.5)
    square_list = np.zeros([N,N])
    for i in range(N):
        for j in range(N):
            square_list[i,j] = vec[i+N*j]
    return square_list

def solveNetworkLP(N,edgeCosts,edgeMaxFlows,sources,sinks):
    c = flatten(edgeCosts)
    A_ub = None
    b_ub = None

    A_eq = np.zeros([N,N*N])
    for i in range(N):
        Adum = np.zeros([N,N])
        for j in range(N):
            Adum[i,:] = -1
            Adum[:,i] = 1
            Adum[i,i] = 0
        A_eq[i,:] = flatten(Adum)

    b_eq = np.array(sources) - np.array(sinks)
    bounds = [(0,j) for sublist in edgeMaxFlows for j in sublist]

    solution = scipy.optimize.linprog(c, A_ub, b_ub, A_eq, b_eq, bounds)

    # Giving same dict output as GP solve
    flow = square(solution['x'])
    solDict = {}
    solDict['flow'] = flow
    return solDict

