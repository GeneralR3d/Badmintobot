import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

TIME_INTERVAL = 1/30
features = [
    'time',
    'LocationX',
    'LocationY',
    'LocationZ',
    'LaunchX',
    'LaunchY',
    'LaunchZ',
    'LaunchAngle',
    'LaunchDirection',
    'InitialV',
    'label'
]

def main():
    dataset= pd.read_excel("../testData/Vision Trajectory3.xlsx", sheet_name = ['forward3_out',
                                                                                'forward7_out',
                                                                                'forward6_scaled',
                                                                                'forward7_scaled',
                                                                                'shot1_away_camera'])
    combinedDF = pd.DataFrame()
    for feature in features:
        combinedDF[feature]= None


    for sheet in dataset:
        print(sheet)
        # get each sheet
        DF = dataset[sheet]
        DF= DF[DF['Ball']==1]

        # create temporary dataframe and populate it with features
        tempDF = pd.DataFrame()
        for feature in features:
            tempDF[feature]= None
        tempDF['LocationX'] = DF['y'] * 10
        tempDF['LocationY'] = DF['x'] * 10
        tempDF['LocationZ'] = DF['z'] * 10
        tempDF=findStart(tempDF) # overwrite
        #tempDF.set_index(drop=True)
        print(tempDF)
        tempDF['time'] = np.arange(0.0,len(tempDF)*TIME_INTERVAL,TIME_INTERVAL)
        tempDF['label'] = list(dataset.keys()).index(sheet)+1
        combinedDF=pd.concat([combinedDF,tempDF],ignore_index=True)

    combinedDF.to_excel('datasetModified.xlsx',index=False)

def findStart(dataframe):
    '''
    Find the true start point of a trajectory by looking at acceleration values between each of the points.
    The true start is the first frame when the shuttlecock has just left the racket. Assume that happens when shuttlecock reaches its max instantaneous velocity.
    Then the true start point should be the i+1 point! Since the speed btwn i+2 and i+1 is less than btwn i+1 and i, it makes sense that
    shuttlecock left at i+1!
    '''
    speeds = []
    # we minus one since we are unable to access the coordinates at t+1 for the very last row, DNE! 
    for i in range(len(dataframe)-1):
        row = dataframe.iloc[i]
        nextRow = dataframe.iloc[i+1]
        forwardSpeed = (math.sqrt((nextRow['LocationX'] - row['LocationX'])**2 + 
                                  (nextRow['LocationY'] - row['LocationY'])**2 +
                                  (nextRow['LocationZ'] - row['LocationZ'])**2)) /(TIME_INTERVAL)
        speeds.append((forwardSpeed,i,i+1))
    speeds.sort(key= lambda x:x[0],reverse=True)
    trueStartIndex = speeds[0][2]
    return dataframe[trueStartIndex:]

def plotSpeeds(dataframe):
    '''
    Calculates and plots instantaneous speed of shuttlecock between every frame
    '''
    speeds = []
    # we minus one since we are unable to access the coordinates at t+1 for the very last row, DNE! 
    for i in range(len(dataframe)-1):
        row = dataframe.iloc[i]
        nextRow = dataframe.iloc[i+1]
        forwardSpeed = (math.sqrt((nextRow['LocationX'] - row['LocationX'])**2 + 
                                  (nextRow['LocationY'] - row['LocationY'])**2 +
                                  (nextRow['LocationZ'] - row['LocationZ'])**2)) /(TIME_INTERVAL)
        
        speeds.append(forwardSpeed)
    fig = plt.Figure()
    plt.plot(speeds)
    plt.xlabel('Frame')
    plt.ylabel('Speed')
    plt.title('Instantaneous speed of shuttlecock at each frame')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
