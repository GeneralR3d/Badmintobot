import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

dataset = pd.read_excel("Vision Trajectory.xlsx")
x = dataset["x"]
y = dataset["y"]
z = dataset["z"]

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
ax.scatter(x, y, z, c='b', marker='o')

# Set labels for the axes
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Set a title
ax.set_title('3D Scatter Plot')

# Show the plot
plt.show()