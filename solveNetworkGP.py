from gpkit import Variable, VectorVariable, Model, SignomialsEnabled, SignomialEquality
from gpkit.constraints.bounded import Bounded
from flow import Flow

def solveNetworkGP(N,edgeCosts,edgeMaxFlows,sources,sinks):
    m = Flow(N)
    m.substitutions.update({
        'edgeCost':       edgeCosts,
        'edgeMaxFlow':    edgeMaxFlows,
        'source'     :    sources,
        'sink'       :    sinks,
        })
    m = Model(m.variables_byname('totalCost')[0], Bounded(m))
    sol = m.localsolve(verbosity=4, reltol=10**-5,iteration_limit=100)
    return sol