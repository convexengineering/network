from gpkit import Variable, VectorVariable, Model, SignomialsEnabled, SignomialEquality
from gpkit.constraints.bounded import Bounded
from flow import Flow
from relaxed_constants import relaxed_constants
import numpy as np

def solveNetworkGP(N,edgeCosts,edgeMaxFlows,sources,sinks):
    m = Flow(N)
    m.substitutions.update({
        'edgeCost':       edgeCosts,
        'edgeMaxFlow':    edgeMaxFlows,
        'source'     :    sources,
        'sink'       :    sinks,
        })
    m.substitutions.update({'slackCost': 1000})#['sweep',np.linspace(100,10000,10)]})
    m.cost = np.sum(m['edgeCost'] * m['flow']) + m['slackCost']*np.prod(m['slack'])
    m = relaxed_constants(m)
    sol = m.localsolve(verbosity=4, reltol=10**-5,iteration_limit=100)
    return sol