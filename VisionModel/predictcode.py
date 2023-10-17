import pandas as pd
import numpy as np
import pickle
import math

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

############################################################################################################

TIME_INTERVAL = 1/30
end_time = 2


time_points = np.arange(0, end_time + TIME_INTERVAL, TIME_INTERVAL)

dataset = pd.read_excel("../testData/Vision Trajectory3.xlsx",'Trajectory 1')
correctedDF = pd.DataFrame()

# The flipping of X and Y axes is done here


# magicStartFrame = 0
# xData = dataset[(dataset["Ball"]==1) & (dataset["Frame"]>=magicStartFrame)]["y"]
# yData = dataset[(dataset["Ball"]==1) & (dataset["Frame"]>=magicStartFrame)]["x"]
# zData = dataset[(dataset["Ball"]==1) & (dataset["Frame"]>=magicStartFrame)]["z"]

# xData=xData.reset_index(drop=True)
# yData=yData.reset_index(drop=True)
# zData=zData.reset_index(drop=True)

correctedDF["LocationX"] = dataset["y"] *10
correctedDF["LocationY"] = dataset["x"] *10
correctedDF["LocationZ"] = dataset["z"] *10
#correctedDF=findStart(correctedDF)  
#correctedDF = correctedDF.set_index(drop=True,keys=np.arange(0,len(correctedDF))) #reset the index to start from 0, keys is an array/iterator of index values, same size as df itself




#In vision trajectory 
# X is wrt width of court
# Y is wrt length of court
# Z is wrt height of court

#Extraction of key values from arrays to feed to into model

LaunchX= correctedDF["LocationX"][10]
LaunchY= correctedDF["LocationY"][10]
LaunchZ= correctedDF["LocationZ"][10]
changeX= (correctedDF["LocationX"][1]-correctedDF["LocationX"][0])
changeY= (correctedDF["LocationY"][1]-correctedDF["LocationY"][0])
changeZ= (correctedDF["LocationZ"][1]-correctedDF["LocationZ"][0])

print(LaunchX)
print(LaunchY)
print(LaunchZ)


def main():
    # Load the trained model
    with open('models/trained_modelX.pkl', 'rb') as file:
        gbm = pickle.load(file)
        pred_gbm=predictData(gbm)

        # Output the predicted data
        predicted_data = pd.DataFrame({
            "time": time_points,
            "LocationX": pred_gbm
        })
        predicted_data.to_excel("output/predicted_trajectoriesX.xlsx", index=False)

    # Load the trained model
    with open('models/trained_modelY.pkl', 'rb') as file:
        gbm = pickle.load(file)
        pred_gbm=predictData(gbm)

        # Output the predicted data
        predicted_data = pd.DataFrame({
            "time": time_points,
            "LocationY": pred_gbm
        })
        predicted_data.to_excel("output/predicted_trajectoriesY.xlsx", index=False)

    # Load the trained model
    with open('models/trained_modelZ.pkl', 'rb') as file:
        gbm = pickle.load(file)
        pred_gbm=predictData(gbm)

        # Output the predicted data
        predicted_data = pd.DataFrame({
            "time": time_points,
            "LocationZ": pred_gbm
        })
        predicted_data.to_excel("output/predicted_trajectoriesZ.xlsx", index=False)



#Iznput
# input_data = pd.DataFrame({
#     "time": time_points,
#     "LaunchX": 200,
#     "LaunchY": 50,
#     "LaunchZ": 1800,
#     "LaunchAngle": 40,
#     "LaunchDirection": 15,
#     "InitialV": 100
# })
def predictData(gbm):

    input_data = pd.DataFrame({
        "time": time_points,    
        "LaunchX": LaunchX, #note these can be swapped cos in the trained model X is wrt to court
        "LaunchY": LaunchY,
        "LaunchZ": LaunchZ,
        "LaunchAngle": math.atan((changeZ)/(math.sqrt(changeX**2 + changeY**2))) * (180/math.pi),
        #calculate from arctan(opp/adj) which is arctan(changez/change in xandy) which is arctan(changez/sqrt(changex^2 + changey^2))
        #essentially calculated from a rotation around the y-axis
        "LaunchDirection": (math.atan((changeY)/(math.sqrt(changeX**2 + changeZ**2))) * (180/math.pi)),
            #calculate from arctan(opp/adj) which is arctan(change in x/change in yandz) which is arctan( changex/sqrt(changey^2 + changez^2)
            #calculated from a rotation around the z-axis
        "InitialV": (math.sqrt(changeX**2 + changeY**2 + changeZ**2)/TIME_INTERVAL)/1000

            #calcuate from change in the 3d position over change in time period
            #recall velocity is a vector so the initialV can only be length of that vector
            #vector is a difference in all 3 coordinates
    })
    y_pred_gbm = gbm.predict(input_data)
    
    return y_pred_gbm



#existing_data = pd.read_excel("predicted_trajectories.xlsx")

#existing_data['LocationY'] = y_pred_gbm

#existing_data.to_excel("predicted_trajectories.xlsx", index=False)

if __name__ == "__main__":
    main()