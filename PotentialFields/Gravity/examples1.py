import matplotlib.pyplot as plt

import construct_field

point_anoms = [
	(5, 5, 1000),
	(175, 150, 10000),
	(100, 17.3, 250),
	(405, 8, 1250),
	(225, 28, 2250)
	]

field = construct_field.Field1D(0, 500, 0.1)
for i in range(0, len(point_anoms)):
	field.add_point_anomaly(point_anoms[i][0], \
						 point_anoms[i][1], \
						 point_anoms[i][2])

plt.plot(field.x, field.grav_field)