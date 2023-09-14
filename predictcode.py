import pandas as pd
import numpy as np
import pickle
import math

# Load the trained model
with open('trained_model.pkl', 'rb') as file:
    gbm = pickle.load(file)

time_interval = 0.01
end_time = 2

time_points = np.arange(0, end_time + time_interval, time_interval)
# time=[]
# i=0
# flag=2
# endTime=1.9
# while i < endTime:
#     if flag%3==0:
#         i+=0.04
#     else:
#         i+=0.03
#     flag+=1
#     time.append(i)
# time_points=np.array(time)

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

visionTraj=pd.read_excel("Vision Trajectory2.xlsx")

#In vision trajectory 
# X is wrt width of court
# Y is wrt length of court
# Z is wrt height of court
LaunchX= visionTraj["x"][0]
LaunchY= visionTraj["y"][0]
LaunchZ= visionTraj["z"][0]
changeX= visionTraj["x"][1]-visionTraj["x"][0]
changeY= visionTraj["y"][1]-visionTraj["y"][0]
changeZ= visionTraj["z"][1]-visionTraj["z"][0]

input_data = pd.DataFrame({
    "time": time_points,
    "LaunchX": LaunchX, #note these can be swapped cos in the trained model X is wrt to court
    "LaunchY": LaunchY,
    "LaunchZ": LaunchZ,
    "LaunchAngle": math.atan((changeZ)/(math.sqrt(changeX**2 + changeY**2))) * (180/math.pi),
      #calculate from arctan(opp/adj) which is arctan(changez/change in xandy) which is arctan(changez/sqrt(changex^2 + changey^2))
      #essentially calculated from a rotation around the y-axis
    "LaunchDirection": math.atan((changeX)/(math.sqrt(changeY**2 + changeZ**2))) * (180/math.pi),
        #calculate from arctan(opp/adj) which is arctan(change in x/change in yandz) which is arctan( changex/sqrt(changey^2 + changez^2)
        #calculated from a rotation around the z-axis
    "InitialV": 
        #calcuate from change in the 3d position over change in time period
        #recall velocity is a vector so the initialV can only be length of that vector
        #vector is a 
})


y_pred_gbm = gbm.predict(input_data)

# Output the predicted data
predicted_data = pd.DataFrame({
    "time": input_data["time"],
    "LocationX": y_pred_gbm
})

predicted_data.to_excel("predicted_trajectories.xlsx", index=False)
#existing_data = pd.read_excel("predicted_trajectories.xlsx")

#existing_data['LocationY'] = y_pred_gbm

#existing_data.to_excel("predicted_trajectories.xlsx", index=False)