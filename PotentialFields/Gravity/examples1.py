import matplotlib.pyplot as plt

import construct_field

field = construct_field.Field2D(0, 200, 0, 200, 1, 1)

field.add_point_anomaly(100, 100, 15, 1000)

plt.pcolor(field.x, field.y, field.grav_field)