import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

dataset = pd.read_excel("Vision Trajectory2.xlsx")
x = dataset["y"]*10
y = dataset["x"]*10
z = dataset["z"]*10

fromModel= pd.read_excel("predicted_trajectories_combined.xlsx")
modelX=fromModel["LocationX"]
modelY=fromModel["LocationY"]
modelZ=fromModel["LocationZ"]

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
ax.scatter(x, y, z, c='b', marker='o')
ax.scatter(modelX, modelY, modelZ, c='r', marker='o')


# Set labels for the axes
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Set a title
ax.set_title('3D Scatter Plot')

# Show the plot
plt.show()