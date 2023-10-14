import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

# read from test data


'''With no magic frame'''
dataset = pd.read_excel("testData/Vision Trajectory3.xlsx",'Trajectory 1')
x = dataset["y"]
y = dataset["x"]
z = dataset["z"]

'''With magic frame for plotting points that are not yet fed into the ML model'''
# magicStartFrame = 0
# dataset1 = pd.read_excel("testData/Vision Trajectory3.xlsx",'forward6_scaled')
# x1 = dataset1[(dataset1["Ball"]==1) & (dataset1["Frame"]>=magicStartFrame)]["y"]
# y1 = dataset1[(dataset1["Ball"]==1) & (dataset1["Frame"]>=magicStartFrame)]["x"]
# z1 = dataset1[(dataset1["Ball"]==1) & (dataset1["Frame"]>=magicStartFrame)]["z"]


# scale each array by 10 to convert to mm
x = x * 10
y = y * 10
z = z * 10
# x1*=10
# y1*=10
# z1*=10


#read from predicted data
modelX= pd.read_excel("VisionModel/output/predicted_trajectoriesX.xlsx")["LocationX"]
modelY= pd.read_excel("VisionModel/output/predicted_trajectoriesY.xlsx")["LocationY"]
modelZ= pd.read_excel("VisionModel/output/predicted_trajectoriesZ.xlsx")["LocationZ"]


# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Scatter plot
ax.scatter(x, y, z, c='b', marker='o',label='actual')
#ax.plot(x1, y1, z1, c='b', marker='o')
# ax.scatter(x3, y3, z3, c='y', marker='o')
ax.plot(modelX, modelY, modelZ, c='r', marker='o',label='predicted')


# Set labels for the axes
ax.set_xlabel('Length of court')
ax.set_ylabel('Width of court')
ax.set_zlabel('Height of court')

#set the spacing
ax.set_xlim(0, 14_000)
ax.set_ylim(-3000, 3000)
ax.set_zlim(0, 5000)

# Set a title
ax.set_title('Trajectory 1')

# Show the plot
plt.show()