import numpy as np 

class MassObject(object):
	"""
	Class to create a massive object with its own gravitational
	potential field. Object is treated as a point mass.
	"""
	def __init__(self, mass):
		"""
		
		"""
		self.mass = mass
		
	def potential(self, radius):
		"""
		Calculate the gravitational potential, U = Gm/r, 
		of the object.
		
		Inputs:
			radius (float or int): the radius at which to calculate
				potential.
		
		Returns:
			potential (float): the gravitational potential field
				strength at the radius.
		"""
		G = 6.67*(10**-11)
		return (G*self.mass)/(radius)
	
class Field1D(object):
	"""
	Class to create a 1-D gravitational field survey line, mass objects can be
	added at any positions and depths along the length of the survey line.
	"""
	def __init__(self, xmin, xmax, deltax):
		self.xmin = xmin
		self.xmax = xmax
		self.x = np.arange(xmin, xmax+deltax, deltax)
		self.grav_field = self.background()
		
	def background(self, amplitude=9.8, noise=False):
		if noise == False:
			return amplitude*np.ones(len(self.x))
		elif noise == True:
			return amplitude*np.ones(len(self.x)) + np.random.rand(len(self.x))
		
	def add_point_anomaly(self, xpos, depth, mass):
		x = self.x
		obj = MassObject(mass)
		grav_potent = np.zeros(len(x))
		for ix in range(0, len(x)):
			radius = ((x[ix] - xpos)**2 + depth**2)**0.5
			grav_potent[ix] = obj.potential(radius)
		self.grav_field = self.grav_field + grav_potent
	