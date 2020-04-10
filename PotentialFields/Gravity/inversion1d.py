
import numpy as np

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

def gradient_descent(inverter, xpos, depth, mass_init, rate, progress=True, iterations=None):
	mass = mass_init
	inverter.calc_misfit(xpos, depth, mass) # calculate initial conditions
	misfit = inverter.misfit

	misfits = []
	masses = []
	i = -1
	while True:
		i = i + 1
		# update mass and misfit values
		mass = mass - rate*np.sum((inverter.model - inverter.observed))
		inverter.calc_misfit(xpos, depth, mass)
		misfit = inverter.misfit
		# calculate change in misfit with previous iteration
		if i == 0:
			misfit_change = 0
		else:
			misfit_change = ((misfit - misfits[-1])/misfits[-1])*100
		# append to list for plotting later
		misfits.append(misfit)
		masses.append(mass)

		if progress == True:
			print('Iteration {}: Mass = {}, Misfit = {}'.format(i, mass, misfit))

		# if change in misfit decreases, break loop, inversion solved!
		if i == iterations:
			break
		elif i > 0:
			if misfit_change > -0.05:
				break
	return np.asarray(misfits), np.asarray(masses)

class Invert(object):
	
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