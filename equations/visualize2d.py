import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D





dataset = pd.read_excel("LOL.xlsx")
t = dataset["time"]
y = dataset["y"]
z = dataset["z"]


ref = pd.read_excel("Joel Camera Trajectory_Image4.xlsx")
location_x = ref["location_xM"]
location_z = ref["location_zM"]






# Create a 2D scatter plot
fig = plt.figure()
ax = fig.add_subplot()


# Scatter plot
#ax.plot(y,z, c='b', marker='o',label='actual')

#ax.plot(t,speed, c='r', marker='o',label='speed')
ax.plot(y,z, c='b', marker='o',label='calculated')
ax.plot(location_x,location_z, c='r', marker='o',label='actual')
# ax.scatter(x3, y3, z3, c='y', marker='o')
#ax.plot(model["LocationX"], model["LocationY"], model["LocationZ"], c='r', marker='o',label='predicted')


# Set labels for the axes
ax.set_xlabel('Length of court')
ax.set_ylabel('Height')
ax.legend()
# ax.set_xlabel('time')
# ax.set_ylabel('velocity')
#set the spacing
# ax.set_xlim(0, 14_000)
# ax.set_ylim(-3000, 3000)

# Set a title
ax.set_title("Graph of Predicted and Experimental trajectories using equations of motion")

# Show the plot
plt.show()