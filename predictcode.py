import pandas as pd
import numpy as np
import pickle
import math

time_interval = 1/30
end_time = 2

time_points = np.arange(0, end_time + time_interval, time_interval)

dataset = pd.read_excel("testSet/Vision Trajectory3.xlsx",'forward6_scaled')

# The flipping of X and Y axes is done here


magicStartFrame = 26
xData = dataset[(dataset["Ball"]==1) & (dataset["Frame"]>=magicStartFrame)]["y"]
yData = dataset[(dataset["Ball"]==1) & (dataset["Frame"]>=magicStartFrame)]["x"]
zData = dataset[(dataset["Ball"]==1) & (dataset["Frame"]>=magicStartFrame)]["z"]

xData=xData.reset_index(drop=True)
yData=yData.reset_index(drop=True)
zData=zData.reset_index(drop=True)

# xData = dataset["y"]
# yData = dataset["x"]
# zData = dataset["z"]



#In vision trajectory 
# X is wrt width of court
# Y is wrt length of court
# Z is wrt height of court

#Extraction of key values from arrays to feed to into model
LaunchY= yData[0] * 10
LaunchX= xData[0] * 10
LaunchZ= zData[0] * 10
changeY= (yData[1]-yData[0]) *10
changeX= (xData[1]-xData[0]) *10
changeZ= (zData[1]-zData[0]) *10
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
        "LaunchX": LaunchY, #note these can be swapped cos in the trained model X is wrt to court
        "LaunchY": LaunchX,
        "LaunchZ": LaunchZ,
        "LaunchAngle": math.atan((changeZ)/(math.sqrt(changeX**2 + changeY**2))) * (180/math.pi),
        #calculate from arctan(opp/adj) which is arctan(changez/change in xandy) which is arctan(changez/sqrt(changex^2 + changey^2))
        #essentially calculated from a rotation around the y-axis
        "LaunchDirection": (math.atan((changeY)/(math.sqrt(changeX**2 + changeZ**2))) * (180/math.pi)),
            #calculate from arctan(opp/adj) which is arctan(change in x/change in yandz) which is arctan( changex/sqrt(changey^2 + changez^2)
            #calculated from a rotation around the z-axis
        "InitialV": (math.sqrt(changeX**2 + changeY**2 + changeZ**2)/time_interval)/1000
            #calcuate from change in the 3d position over change in time period
            #recall velocity is a vector so the initialV can only be length of that vector
            #vector is a difference in all 3 coordinates
    })
    y_pred_gbm = gbm.predict(input_data)
    
    return y_pred_gbm


#existing_data = pd.read_excel("predicted_trajectories.xlsx")

#existing_data['LocationY'] = y_pred_gbm

#existing_data.to_excel("predicted_trajectories.xlsx", index=False)

main()