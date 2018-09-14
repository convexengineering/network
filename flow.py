from gpkit import Model, Variable, VectorVariable, SignomialsEnabled
from gpkit.constraints.tight import Tight
import numpy as np


class Flow(Model):
    def setup(self, N):
        edgeCost = VectorVariable([N, N],
                                  'edgeCost')
        edgeMaxFlow = VectorVariable([N, N],
                                     'edgeMaxFlow')
        slackCost = Variable('slackCost', 1000)
        connect = VectorVariable([N, N], 'connectivity')
        flow = VectorVariable([N, N], 'flow')
        source = VectorVariable(N, 'source')
        sink = VectorVariable(N, 'sink')
        slack_one = VectorVariable(N, 'slackOne')
        slack_two = VectorVariable(N, 'slackTwo')
        constraints = []

        with SignomialsEnabled():

            for i in range(0, N):
                constraints.extend([
                    Tight([sink[i] + sum(flow[i, :]) <= slack_one[i]*(source[i] + sum(flow[:, i]))]),
                    Tight([slack_one[i] >= 1]),
                    Tight([source[i] + sum(flow[:, i]) <= slack_two[i] * (sink[i] + sum(flow[i, :]))]),
                    Tight([slack_two[i] >= 1]),
                ])
                for j in range(0, N):
                    constraints += [flow[i, j] <= connect[i, j] * edgeMaxFlow[i, j],
                                    connect[i, j] <= 1.,
                                    flow[i, j] >= 1e-20]
            for i in range(0, N):
                for j in range(i + 1, N):
                    constraints.extend([connect[i, j] * connect[j, i] <= 1e-20])
        return constraints
