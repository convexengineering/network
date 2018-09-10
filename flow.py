from gpkit import Model, Variable, VectorVariable, SignomialsEnabled
from gpkit.constraints.tight import Tight
import numpy as np

class Flow(Model):
    def setup(self, N):
        edgeCost = VectorVariable([N, N],
                                  'edgeCost')
        edgeMaxFlow = VectorVariable([N, N],
                                     'edgeMaxFlow')
        slackCost = Variable('slackCost',1000)
        connect = VectorVariable([N,N],'connectivity')
        flow = VectorVariable([N, N], 'flow')
        source = VectorVariable(N, 'source')
        sink = VectorVariable(N, 'sink')
        #slack = VectorVariable(N, 'slack')

        constraints = []

        with SignomialsEnabled():

            for i in range(0, N):
                constraints.extend([
                    Tight([sink[i] + sum(flow[i, :]) <= (source[i] + sum(flow[:, i]))]),
                    #Tight([slack[i] >= 1])
                    ])
                for j in range(0, N):
                    constraints += [flow[i, j] <= connect[i,j]*edgeMaxFlow[i, j],
                                    connect[i,j] <= 1.,
                                    flow[i,j] >= 1e-20,
                                    edgeCost[i,j] >= 1e-20]
            for i in range(0, N):
                for j in range(i + 1, N):
                    constraints.extend([connect[i, j] * connect[j, i] <= 1e-20])
        return constraints
