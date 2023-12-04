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
# we need to associate each "difference" feature, 'diffX','diffY','diffZ','diffAngle','diffDirection','vDiff' to the i+1 time stamp not i
# This means that arrow is pointing forward from first coordinate to second coordinate, but now its tagged at the second coordinate instead
# 1) If we dont do so we are actually leaking data into the "future" when doing past covariates in time series regression
# 2) It makes more sense for the first value of each "difference" feature to be 0, where 2 points havent existed to calculate the difference, than the last coordinate
# the very 1st value of each difference feature can either be 0 or NaN
for labelNo in dataset['label'].unique():
    currentDF=dataset[dataset['label']==labelNo]
    firstIndex = currentDF.index[0]

    diffX = pd.Series([currentDF['LocationX'][i] - currentDF['LocationX'][i-1] for i in range(firstIndex+1,firstIndex+len(currentDF))])
    diffX = pd.concat([pd.Series([0]),diffX],ignore_index=True)
    diffX.index = currentDF.index
    currentDF['diffX'] = diffX

    diffY = pd.Series([currentDF['LocationY'][i] - currentDF['LocationY'][i-1] for i in range(firstIndex+1,firstIndex+len(currentDF))])
    diffY = pd.concat([pd.Series([0]),diffY],ignore_index=True)
    diffY.index = currentDF.index
    currentDF['diffY'] = diffY

    diffZ = pd.Series([currentDF['LocationZ'][i] - currentDF['LocationZ'][i-1] for i in range(firstIndex+1,firstIndex+len(currentDF))])
    diffZ = pd.concat([pd.Series([0]),diffZ],ignore_index=True)
    diffZ.index = currentDF.index
    currentDF['diffZ'] = diffZ

    diffAngle = pd.Series([math.atan((currentDF['diffZ'][i])/(math.sqrt(currentDF['diffX'][i]**2 + currentDF['diffY'][i]**2))) * (180/math.pi) for i in range(firstIndex+1,firstIndex+len(currentDF))])
    diffAngle = pd.concat([pd.Series([0]),diffAngle],ignore_index=True)
    diffAngle.index = currentDF.index
    currentDF['diffAngle'] = diffAngle

    diffDirection = pd.Series([math.atan((currentDF['diffY'][i])/(math.sqrt(currentDF['diffX'][i]**2 + currentDF['diffZ'][i]**2))) * (180/math.pi) for i in range(firstIndex+1,firstIndex+len(currentDF))])
    diffDirection = pd.concat([pd.Series([0]),diffDirection],ignore_index=True)
    diffDirection.index = currentDF.index
    currentDF['diffDirection'] = diffDirection

    vDiff= pd.Series([((math.sqrt(currentDF['diffX'][i]**2 + currentDF['diffY'][i]**2 + currentDF['diffZ'][i]**2)/time_interval)/1000) for i in range(firstIndex+1,firstIndex+len(currentDF))])
    vDiff = pd.concat([pd.Series([0]),vDiff],ignore_index=True)
    vDiff.index = currentDF.index
    currentDF['vDiff'] = vDiff

    dataset.update(currentDF)

dataset.to_excel("datasetFilledDynamicFeatures.xlsx",index=False)
