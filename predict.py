import pandas as pd
import numpy as np
import pickle
import math

time_interval = 1/30
end_time = 2

time_points = np.arange(0, end_time + time_interval, time_interval)

dataset = pd.read_excel("testSet/Vision Trajectory3.xlsx",'Trajectory 1')






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
        "LaunchX": 0, #note these can be swapped cos in the trained model X is wrt to court
        "LaunchY": 0,
        "LaunchZ": 1900,
        "LaunchAngle": 60,
        #calculate from arctan(opp/adj) which is arctan(changez/change in xandy) which is arctan(changez/sqrt(changex^2 + changey^2))
        #essentially calculated from a rotation around the y-axis
        "LaunchDirection":0,
            #calculate from arctan(opp/adj) which is arctan(change in x/change in yandz) which is arctan( changex/sqrt(changey^2 + changez^2)
            #calculated from a rotation around the z-axis
        "InitialV": 100

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