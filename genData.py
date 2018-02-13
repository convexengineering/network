import numpy as np
import random as rn
from matplotlib import pyplot as plt
import csv
import collections

# Generating data for minimum spanning tree problem in R2 [-1 < x,y < 1]

def genMST(xRange, yRange, Npoints):
	points = np.zeros((Npoints,2))
	euclidianDistances = np.zeros((Npoints,Npoints))
	for i in range(Npoints):
		points[i,:] = [rn.uniform(xRange[0],xRange[1]),rn.uniform(yRange[0],yRange[1])]

	for i in range(Npoints):
		for j in range(Npoints):
			euclidianDistances[i,j] = np.linalg.norm(points[i,:] - points[j,:],ord=2)

	return points, euclidianDistances

if __name__ == '__main__':
	xRange = (-1, 1)
	yRange = (-1, 1)
	Npoints = 10

	points, euclidianDistances = genMST(xRange,yRange,Npoints)
	np.savetxt('points.csv', (points), delimiter=',')
	np.savetxt('eucDist.csv', (euclidianDistances), delimiter=',')



	plt.xlim(xRange)
	plt.ylim(yRange)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.plot(points[:,0],points[:,1],'r*')
