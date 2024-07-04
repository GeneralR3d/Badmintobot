import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import math

df= pd.read_csv("2.csv")
matrix = df.values
x = df["x"]
y = df["y"]
z = df["z"]

#angleRad = math.atan((2.336129236221313477e+03 - 2.953406143188476562e+03)/(3.481303167343139648e+03 - 1.051136560440063477e+04))
angleRad = math.atan2((2.336129236221313477e+03 - 2.953406143188476562e+03),(3.481303167343139648e+03 - 1.051136560440063477e+04))
newy = -((y-1.051136560440063477e+04)/math.cos(angleRad))
x0= np.zeros(x.size)

#newy=y*math.cos(angleRad)

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlim([0,3000])
ax.set_ylim([0,11000])
ax.set_zlim([0,6000])



ax.plot(x,y,z, c='b', marker='o',label='IR')
ax.plot(x0,newy,z, c='r', marker='o',label='IR')
#ax.quiver(matrix[0,0],matrix[0,1],matrix[0,2],matrix[1,0],matrix[1,1],matrix[1,2])
print(np.linspace(0,9,10))
# X,Y = np.meshgrid(np.linspace(0,9,10),np.linspace(0,9,10))
# ax.plot_surface(X,Y,X)
plt.show()