import numpy as np
import matplotlib.pyplot as plt

import construct_field

def background_removal(signal, background_amp):
	background = background_amp*np.ones(signal.shape)
	return signal - background

class Invert1D(object):
	
	def __init__(self, x, signal):
		self.x = x
		self.observed = signal
		self.misfit = None
		
	def forward(self, xpos, depth, mass):
		x = self.x
		obj = construct_field.MassObjectPoint(mass)
		model = np.zeros(len(x))
		for ix in range(0, len(x)):
			radius = ((x[ix] - xpos)**2 + depth**2)**0.5
			model[ix] = obj.potential(radius)
		self.model = model
	
	def calc_misfit(self, xpos, depth, mass):
		self.forward(xpos, depth, mass)
		misfit = ((1/len(self.model))*np.sum((self.observed - self.model)**2))**0.5
		self.misfit = misfit
			

# create an example 1-D dataset
field = construct_field.Field1D(0, 300, 1)
field.add_point_anomaly(125, 35, 100000)
x = field.x
signal = field.grav_field

# do the background removal
signal_anom = background_removal(signal, background_amp=9.8)

inverter = Invert1D(x, signal_anom)
depth = 35
xpos = 125
mass = np.arange(1000, 20000, 100)
misfits = np.zeros(len(mass))
for imass in range(0, len(mass)):
	inverter.calc_misfit(xpos, depth, mass[imass])
	misfits[imass] = inverter.misfit