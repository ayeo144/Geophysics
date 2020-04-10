import time
import numpy as np
import matplotlib.pyplot as plt

import construct_field

def background_removal(signal, background_amp):
	background = background_amp*np.ones(signal.shape)
	return signal - background

def grid_search(inverter, xpos, depth, mass):
	misfits = np.zeros(len(mass))
	for imass in range(0, len(mass)):
		inverter.calc_misfit(xpos, depth, mass[imass])
		misfits[imass] = inverter.misfit
	min_idx = np.argmin(misfits)
	mass_estimate = mass[min_idx]
	mass_estimate_misfit = misfits[min_idx]
	return mass_estimate, mass_estimate_misfit, misfits

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
		# L = 1/n sum (y - p)**2
		self.forward(xpos, depth, mass)
		misfit = np.sum((self.observed - self.model)**2)/len(self.model)
		self.misfit = misfit
			
# create an example 1-D dataset
field = construct_field.Field1D(0, 300, 1)
field.add_point_anomaly(125, 35, 100000)
x = field.x
signal = field.grav_field

# do the background removal
signal_anom = background_removal(signal, background_amp=9.8)

# Solve the Inverse Problem
inverter = Invert1D(x, signal_anom)
depth = 35
xpos = 125

# optimization 1: simple grid search
mass = np.arange(10000, 200000, 1000)
t1 = time.time()
mass_estimate, mass_estimate_misfit, misfits = grid_search(inverter, xpos, depth, mass)
runtime1 = time.time() - t1

# optimization 2: gradient descent
mass = 50000
rate = 100000000

inverter.calc_misfit(xpos, depth, mass)
misfit = inverter.misfit

misfits = []
masses = []
i = -1
t1 = time.time()
while True:
	i = i + 1
	mass = mass - rate*np.sum((inverter.model - inverter.observed))
	inverter.calc_misfit(xpos, depth, mass)
	misfit = inverter.misfit
	
	if i == 0:
		misfit_change = 0
	else:
		misfit_change = ((misfit - misfits[-1])/misfits[-1])*100
	
	misfits.append(misfit)
	masses.append(mass)
	
	if i > 0:
		if misfit_change > -0.05:
			break
runtime2 = time.time() - t1







