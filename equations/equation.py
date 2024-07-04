import numpy as np
import pandas as pd
import math
import time
#Initial Variabales

predictStartTime = time.time()

start_time = 0
time_step = 1/30
end_time = 2

G=9.81
mass_shuttle = 5.12/1000
#viscocity_air = 0.0000182
coef_drag = 0.4
diameter = 0.05
density_air = 1.18
density_shuttle = 30


# start_point = (0,0)
# v_start = 2.3
# launch_angle = np.pi/3

start_point = (0.835263158,2.061315789)
second_point = (3.520263158,3.798947368)
v_start = (math.sqrt((second_point[0] - start_point[0])**2 + (second_point[1] - start_point[1])**2))/time_step
launch_angle = math.atan((second_point[1] - start_point[1])/(second_point[0] - start_point[0]))
#reynolds_num = (np.exp * v_start)/(viscocity_air)

t = np.empty(shape=0)
y_coor = np.empty(shape=0)
z_coor = np.empty(shape=0)
speed = np.empty(shape=0)

t = np.append(t,[0.0])
y_coor = np.append(y_coor,[start_point[0]])
z_coor = np.append(z_coor,[start_point[1]])
speed = np.append(speed,[v_start])

for i in range(int(end_time/time_step)):

    v_start_y = v_start * np.cos(launch_angle)
    v_start_z = v_start * np.sin(launch_angle)

    next_point = (v_start_y*time_step + start_point[0]), (v_start_z*time_step + start_point[1])
    print(next_point)
    t = np.append(t,[(i+1)*time_step])
    y_coor = np.append(y_coor,[next_point[0]])
    z_coor = np.append(z_coor, [next_point[1]])

    v_next_y = (( -(0.5 * coef_drag * density_air * (v_start**2) * ((np.pi * diameter**2)/4)) * np.cos(launch_angle)) 
                * (time_step/mass_shuttle)
                ) + v_start_y

    v_next_z = (((((np.pi * diameter**3 * G)/6) * (density_air - density_shuttle)) - ((0.5 * coef_drag * density_air * (v_start**2) * ((np.pi * diameter**2)/4)) * np.sin(launch_angle))) * 
                (time_step/mass_shuttle)
                ) + v_start_z


    v_next = np.sqrt(v_next_y**2 + v_next_z**2)
    speed = np.append(speed,[v_next])

    launch_angle = np.arctan(v_next_z/v_next_y)
    v_start = v_next
    start_point = next_point

print(y_coor)
print(z_coor)
print(f"Whole prediction takes { time.time() - predictStartTime}sec")
df = pd.DataFrame(data = {
    "t" : t,
    "y" : y_coor,
    "z": z_coor,
    "speed": speed
})
df.to_excel("LOL.xlsx",index=False)



