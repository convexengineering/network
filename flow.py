from gpkit import Model, Variable, VectorVariable, SignomialsEnabled
import numpy as np

class Flow(Model):
    def setup(self, N):
        edgeCost = VectorVariable([N, N],
                                  'edgeCost')
        edgeMaxFlow = VectorVariable([N, N],
                                     'edgeMaxFlow')
        connect = VectorVariable([N,N],'connectivity')
        flow = VectorVariable([N, N], 'flow')
        source = VectorVariable(N, 'source')
        sink = VectorVariable(N, 'sink')
        slack = VectorVariable(N, 'slack')
        totalCost = Variable('totalCost')

        constraints = []

        with SignomialsEnabled():

            for i in range(0, N):
                constraints.extend([sink[i] + sum(flow[i, :]) <= slack[i]*(source[i] + sum(flow[:, i])),
                                    slack[i] >= 1])
                for j in range(0, N):
                    constraints += [flow[i, j] <= connect[i,j]*edgeMaxFlow[i, j],
                                    connect[i,j] <= 1.,]
            for i in range(0, N):
                for j in range(i + 1, N):
                    constraints.extend([connect[i, j] * connect[j, i] <= 1e-20])
        constraints.extend([totalCost >= np.sum(edgeCost * flow) + 1e4*np.prod(slack)])
        return constraints