import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


#NAME='forward6_scaled'
NAME='Trajectory 1'


'''With no magic frame'''

dataset = pd.read_excel("./one_model/output/predicted_trajectoriesCombined.xlsx")
x = dataset["LocationX"]
y = dataset["LocationY"]
z = dataset["LocationZ"]

'''With magic frame for plotting points that are not yet fed into the ML model'''
# magicStartFrame = 0
dataset1 = pd.read_excel("../testData/Vision Trajectory3.xlsx",NAME)
# x1 = dataset1[(dataset1["Ball"]==1) & (dataset1["Frame"]>=magicStartFrame)]["y"]
# y1 = dataset1[(dataset1["Ball"]==1) & (dataset1["Frame"]>=magicStartFrame)]["x"]
# z1 = dataset1[(dataset1["Ball"]==1) & (dataset1["Frame"]>=magicStartFrame)]["z"]
x1 = dataset1["y"]
y1 = dataset1["x"]
z1 = dataset1["z"]


# scale each array by 10 to convert to mm
# x = x * 10
# y = y * 10
# z = z * 10
x1*=10
y1*=10
z1*=10


#read from predicted data
#model= pd.read_excel("output/predicted_trajectories_DartsCombined.xlsx")



# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')


# Scatter plot
ax.plot(x,y,z, c='r', marker='o',label='predicted')
ax.plot(x1, y1, z1, c='b', marker='o', label='actual')
# ax.scatter(x3, y3, z3, c='y', marker='o')
#ax.plot(model["LocationX"], model["LocationY"], model["LocationZ"], c='r', marker='o',label='predicted')


# Set labels for the axes
ax.set_xlabel('Length of court')
ax.set_ylabel('Width of court')
ax.set_zlabel('Height of court')

#set the spacing
ax.set_xlim(0, 14_000)
ax.set_ylim(-3000, 3000)
ax.set_zlim(0, 5000)
ax.legend()

# Set a title
# ax.set_title("One model"+NAME+"without train test split")
ax.set_title("Graph of Predicted and Experimental trajectories using Gradient Boosting Regressor Model")

plt.show()