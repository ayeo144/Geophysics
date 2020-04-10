import time
import numpy as np
import matplotlib.pyplot as plt

import construct_field, inversion1d

# create an example 1-D dataset
field = construct_field.Field1D(0, 300, 1)  
field.add_point_anomaly(125, 35, 100000)
x = field.x
signal = field.grav_field

# do the background removal
signal_anom = inversion1d.background_removal(signal, background_amp=9.8)

# Solve the Inverse Problem
# *with assumptions of object position (x, z)
inverter = inversion1d.Invert(x, signal_anom)
xpos = 125
depth = 35

# optimization 1: simple grid search
mass_array = np.arange(10000, 200000, 1000) # array of mass values to try
t1 = time.time()
mass_estimate1, mass_estimate_misfit1, misfits1 = inversion1d.grid_search(inverter, xpos, depth, mass_array)
runtime1 = time.time() - t1

# optimization 2: gradient descent
mass_init = 50000 # initiall guess at mass value
rate = 10000000 # 'learning rate'
t1 = time.time()
misfits2, mass_estimates2 = inversion1d.gradient_descent(inverter, xpos, depth, mass_init, rate)
runtime2 = time.time() - t1

# plot results
plt.figure()
plt.plot(mass_array, misfits1)
plt.title('Grid Search Misfits')

plt.figure()
plt.plot(mass_estimates2, misfits2)
plt.title('Gradient Descent Misfits')