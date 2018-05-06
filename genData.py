import numpy as np
import random as rn
import matplotlib.pyplot as plt
import csv
import collections

# Generating data for minimum spanning tree problem in R2 [-1 < x,y < 1]

def genData(xRange, yRange, Npoints):
	points = np.zeros([Npoints,2])
	euclidianDistances = np.zeros([Npoints,Npoints])
	edgeCosts = np.zeros([Npoints,Npoints])
	sources = np.zeros(Npoints)
	sinks = np.zeros(Npoints)
	for i in range(Npoints):
		points[i,:] = [rn.uniform(xRange[0],xRange[1]),rn.uniform(yRange[0],yRange[1])]
		sources[i] = rn.uniform(0,1)
		sinks[i] = rn.uniform(0,1)

	# Making sources == sinks
	sinks = sinks * sum(sources) / sum(sinks)

	for i in range(Npoints):
		for j in range(Npoints):
			euclidianDistances[i,j] = np.linalg.norm(points[i,:] - points[j,:],ord=2)
			edgeCosts[i,j] = euclidianDistances[i,j] * rn.uniform(0,2)

	np.savetxt('points.csv',   (points),             delimiter=',')
	np.savetxt('eucDist.csv',  (euclidianDistances), delimiter=',')
	np.savetxt('edgeCosts.csv',(edgeCosts),         delimiter=',')
	np.savetxt('sources.csv',  (sources),            delimiter=',')
	np.savetxt('sinks.csv',    (sinks),              delimiter=',')

	return points, euclidianDistances, edgeCosts, sources, sinks

if __name__ == '__main__':
	xRange = (-1, 1)
	yRange = (-1, 1)
	Npoints = 20

	points, euclidianDistances, edgeCosts, sources, sinks = genData(xRange,yRange,Npoints)
	plt.xlim(xRange)
	plt.ylim(yRange)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.plot(points[:,0],points[:,1],'r*')
