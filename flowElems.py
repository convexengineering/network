from gpkit import Model, Variable, VectorVariable

class Node(Model):
	def setup(self,linkedEdges):
		source = Variable()
		sink = Variable()

class Edge(Model):
	def setup(self,inNode,outNode):
		edgeFlow = Variable('edgeFlow')
