import numpy as np
import pandas as pd
import math

#constant
time_interval=1/30

dataset= pd.read_excel("datasetTBFilled3D.xlsx")

for i in dataset['label'].unique():
    currentDF=dataset[dataset['label']==i]
    firstIndex=currentDF.index[0] #index returns numpy array of indexes in the DF, the first one is simply index 0
    currentDF['LaunchX'] = currentDF['LocationX'][firstIndex]
    currentDF['LaunchY'] = currentDF['LocationY'][firstIndex]
    currentDF['LaunchZ'] = currentDF['LocationZ'][firstIndex]
    changeX=currentDF['LocationX'][firstIndex+1]-currentDF['LocationX'][firstIndex]
    changeY=currentDF['LocationY'][firstIndex+1]-currentDF['LocationY'][firstIndex]
    changeZ=currentDF['LocationZ'][firstIndex+1]-currentDF['LocationZ'][firstIndex]
    currentDF['LaunchAngle'] = math.atan((changeZ)/(math.sqrt(changeX**2 + changeY**2))) * (180/math.pi)
    currentDF['LaunchDirection'] = (math.atan((changeY)/(math.sqrt(changeX**2 + changeZ**2))) * (180/math.pi))
    currentDF['InitialV']=(math.sqrt(changeX**2 + changeY**2 + changeZ**2)/time_interval)/1000
    dataset.update(currentDF)

dataset.to_excel("datasetFilled3D.xlsx",index=False)
