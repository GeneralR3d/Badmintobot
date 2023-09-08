import pandas as pd
import numpy as np
import pickle

# Load the trained model
with open('trained_model.pkl', 'rb') as file:
    gbm = pickle.load(file)

time_interval = 0.01
end_time = 1

time_points = np.arange(0, end_time + time_interval, time_interval)

#Iznput
input_data = pd.DataFrame({
    "time": time_points,
    "LaunchX": 200,
    "LaunchY": 50,
    "LaunchZ": 1800,
    "LaunchAngle": 40,
    "LaunchDirection": 15,
    "InitialV": 100
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