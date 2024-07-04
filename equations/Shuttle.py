import numpy as np
import pandas as pd
import math
import time

class Shuttle:
    def __init__(self,time_step,end_time,coef_drag,diameter,density_shuttle):
        self.start_time = 0
        self.time_step = time_step
        self.end_time = end_time
        self.G=9.81
        self.mass_shuttle = 5.12/1000
        #viscocity_air = 0.0000182
        self.coef_drag = coef_drag
        self.diameter = diameter
        self.density_air = 1.18
        self.density_shuttle = density_shuttle

        self.start_point = (0.835263158,2.061315789)
        self.second_point = (3.520263158,3.798947368)
    # def __init__(self):
    #     self.start_time = 0
    #     self.time_step = 0.05
    #     self.end_time = 2
    #     self.G=9.81
    #     self.mass_shuttle = 5.12/1000
    #     #viscocity_air = 0.0000182
    #     self.coef_drag = 0.53
    #     self.diameter = 0.06
    #     self.density_air = 1.18
    #     self.density_shuttle = 20
        
    #     self.start_point = (0.835263158,2.061315789)
    #     self.second_point = (3.520263158,3.798947368)

    def set_start_point(self,point):
        self.start_point = point

    def set_second_point(self,point):
        self.second_point = point   
    def fly(self):
        v_start = (math.sqrt((self.second_point[0] - self.start_point[0])**2 + (self.second_point[1] - self.start_point[1])**2))/self.time_step
        launch_angle = math.atan((self.second_point[1] - self.start_point[1])/(self.second_point[0] - self.start_point[0]))
        print(v_start)
        print(launch_angle)
        #reynolds_num = (np.exp * v_start)/(viscocity_air)

        t = np.empty(shape=0)
        y_coor = np.empty(shape=0)
        z_coor = np.empty(shape=0)
        speed = np.empty(shape=0)

        t = np.append(t,[0.0])
        y_coor = np.append(y_coor,[self.start_point[0]])
        z_coor = np.append(z_coor,[self.start_point[1]])
        speed = np.append(speed,[v_start])

        for i in range(int(self.end_time/self.time_step)):

            v_start_y = v_start * np.cos(launch_angle)
            v_start_z = v_start * np.sin(launch_angle)

            next_point = (v_start_y*self.time_step + self.start_point[0]), (v_start_z*self.time_step + self.start_point[1])
            print(next_point)
            t = np.append(t,[(i+1)*self.time_step])
            y_coor = np.append(y_coor,[next_point[0]])
            z_coor = np.append(z_coor, [next_point[1]])

            v_next_y = (( -(0.5 * self.coef_drag * self.density_air * (v_start**2) * ((np.pi * self.diameter**2)/4)) * np.cos(launch_angle)) 
                        * (self.time_step/self.mass_shuttle)
                        ) + v_start_y

            v_next_z = (((((np.pi * (self.diameter**3) * self.G)/6) * (self.density_air - self.density_shuttle)) - ((0.5 * self.coef_drag * self.density_air * (v_start**2) * ((np.pi * self.diameter**2)/4)) * np.sin(launch_angle))) * 
                        (self.time_step/self.mass_shuttle)
                        ) + v_start_z
            
            print("vnexty:",v_next_y)
            print("vnextz:",v_next_z)



            v_next = np.sqrt(v_next_y**2 + v_next_z**2)
            print("vnext:",v_next)
            speed = np.append(speed,[v_next])

            launch_angle = np.arctan(v_next_z/v_next_y)
            print("launchAngle:",launch_angle)
            v_start = v_next
            self.start_point = next_point

        # print(y_coor)
        # print(z_coor)
        df = pd.DataFrame(data = {
            "time" : t,
            "y" : y_coor,
            "z": z_coor,
            "speed": speed
        })
        return df


    
    