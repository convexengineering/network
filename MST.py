from gpkit import Model, Variable, VectorVariable

class MST(Model):
    def setup(self, N):
        edgeCost = VectorVariable([N, N],
                                  'edgeCost')
        edgeMaxFlow = VectorVariable([N, N],
                                     'edgeMaxFlow')
        connect = VectorVariable([N,N],'connectivity')
        flow = VectorVariable([N, N], 'flow')
        source = Variable('source')
        sink = VectorVariable(N-1, 'sink')
        totalCost = Variable('totalCost')

        constraints = []

        with SignomialsEnabled():

            for i in range(0, N):
                constraints.extend([sink[i] + sum(flow[i, :]) >= source[i] + sum(flow[:, i]),])
                for j in range(0, N):
                    constraints += [flow[i, j] <= connect[i,j]*edgeMaxFlow[i, j]]
            for i in range(0, N):
                for j in range(i + 1, N):
                    constraints.extend([flow[i, j] * flow[j, i] <= 1e-5])
        constraints.extend([totalCost >= sum(edgeCost * flow)])
        return constraints