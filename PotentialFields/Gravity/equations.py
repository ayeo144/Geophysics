import random
import numpy as np 

class MassObject(object):
	
	def __init__(self, mass):
		self.mass = mass
		
	def potential(self, radius):
		"""
		U = Gm/r
		"""
		G = 6.67*(10**-11)
		return (G*self.mass)/(radius)
	
class Survey1D(object):
	
	def __init__(self, xmin, xmax, deltax):
		self.xmin = xmin
		self.xmax = xmax
		self.x = np.arange(xmin, xmax+deltax, deltax)
		
	def background(self, amplitude, noise=False):
		if noise == False:
			return amplitude*np.ones(len(self.x))
		elif noise == True:
			return amplitude*np.ones(len(self.x)) + np.random.rand(len(self.x))
