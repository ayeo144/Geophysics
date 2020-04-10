import numpy as np 

class MassObject(object):
	"""
	Class to create a massive object with its own gravitational
	potential field. Object is treated as a point mass.
	"""
	def __init__(self, mass):
		"""
		Inputs:
			mass (float or int): mass of point object.
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
		"""
		Define a gravitational field in space, with the field strength
		initially being the background field strength.
		
		Inputs:
			xmin (float or int): starting position.
			
			xmax (float or int): finishing position.
			
			deltax (float or int): increment size.
		"""
		self.xmin = xmin
		self.xmax = xmax
		self.x = np.arange(xmin, xmax+deltax, deltax)
		self.grav_field = self.background()
		
	def background(self, amplitude=9.8):
		"""
		Create the background field of amplitude
		9.8 m/s/s.
		
		Inputs:
			amplitude (float or int): field strength.
			
		Returns:
			background field (numpy array): background field strength of 
				length x.
		"""
		return amplitude*np.ones(len(self.x))

	def add_point_anomaly(self, xpos, depth, mass):
		"""
		Add a point mass object on the survey line and update the
		gravitational field strength.
		
		Inputs:
			xpos (float or int): postion along x-axis to place mass.
			
			depth (float or int): the depth the object is placed at.
			
			mass (float or int): the mass of the object.
		"""
		x = self.x
		obj = MassObject(mass)
		grav_potent = np.zeros(len(x))
		for ix in range(0, len(x)):
			radius = ((x[ix] - xpos)**2 + depth**2)**0.5
			grav_potent[ix] = obj.potential(radius)
		self.grav_field = self.grav_field + grav_potent
	