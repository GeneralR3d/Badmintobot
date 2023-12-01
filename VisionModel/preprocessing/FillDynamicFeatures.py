import numpy as np
import pandas as pd
import math

#constant
time_interval=1/30

dataset= pd.read_excel("datasetTBFilled.xlsx")
dataset.rename(columns={'LaunchX': 'diffX',
                        'LaunchY': 'diffY',
                        'LaunchZ': 'diffZ',
                        'LaunchAngle':'diffAngle',
                        'LaunchDirection':'diffDirection',
                        'InitialV': 'vDiff'
                        },inplace=True)

# dataframe.assign() and dataframe[index] wont work unless the series has same index as the dataframe itself
# series.reindex or series.index setting wont work until theres same number of elements in the series and in the index
for labelNo in dataset['label'].unique():
    currentDF=dataset[dataset['label']==labelNo]
    firstIndex = currentDF.index[0]

    diffX = pd.Series([currentDF['LocationX'][i+1] - currentDF['LocationX'][i] for i in range(firstIndex,firstIndex+len(currentDF)-1)])
    diffX[diffX.size] = 0
    diffX.index = currentDF.index
    currentDF['diffX'] = diffX

    diffY = pd.Series([currentDF['LocationY'][i+1] - currentDF['LocationY'][i] for i in range(firstIndex,firstIndex+len(currentDF)-1)])
    diffY[diffY.size] = 0
    diffY.index = currentDF.index
    currentDF['diffY'] = diffY

    diffZ = pd.Series([currentDF['LocationZ'][i+1] - currentDF['LocationZ'][i] for i in range(firstIndex,firstIndex+len(currentDF)-1)])
    diffZ[diffZ.size] = 0
    diffZ.index = currentDF.index
    currentDF['diffZ'] = diffZ

    diffAngle = pd.Series([math.atan((currentDF['diffZ'][i])/(math.sqrt(currentDF['diffX'][i]**2 + currentDF['diffY'][i]**2))) * (180/math.pi) for i in range(firstIndex,firstIndex+len(currentDF)-1)])
    diffAngle[diffAngle.size] = 0
    diffAngle.index = currentDF.index
    currentDF['diffAngle'] = diffAngle

    diffDirection = pd.Series([math.atan((currentDF['diffY'][i])/(math.sqrt(currentDF['diffX'][i]**2 + currentDF['diffZ'][i]**2))) * (180/math.pi) for i in range(firstIndex,firstIndex+len(currentDF)-1)])
    diffDirection[diffDirection.size] = 0
    diffDirection.index = currentDF.index
    currentDF['diffDirection'] = diffDirection

    vDiff= pd.Series([((math.sqrt(currentDF['diffX'][i]**2 + currentDF['diffY'][i]**2 + currentDF['diffZ'][i]**2)/time_interval)/1000) for i in range(firstIndex,firstIndex+len(currentDF)-1)])
    vDiff[vDiff.size] = 0
    vDiff.index = currentDF.index
    currentDF['vDiff'] = vDiff

    dataset.update(currentDF)

dataset.to_excel("datasetFilledDynamicFeatures.xlsx",index=False)
