from Shuttle import Shuttle

import pandas as pd
import numpy as np


def getExperimental():
    exp = pd.read_excel("Joel Camera Trajectory_Image4.xlsx")
    exp = exp[["time","location_xM","location_zM"]]
    print(exp)
    return exp
def getPred(coef_drag,diameter,density_shuttle):
    shuttle = Shuttle((1/30),0.77,coef_drag,diameter,density_shuttle)
    pred = shuttle.fly()[["time","y","z"]]
    print(pred)
    return pred
def calError(exp,pred):
    if exp.size != pred.size:
        raise Exception("Size mismatch!")
    mergeDF = pd.merge(exp,pred,on="time")
    mergeDF["error"] = mergeDF.apply(lambda row: (row['location_xM'] - row['y'])**2 + (row['location_zM'] - row['z'])**2,axis=1)
    print(mergeDF["error"])
    return mergeDF["error"].sum()
def main():
    lossArray = np.empty(shape=0)
    density_shuttle_arr = np.empty(shape=0)
    coef_drag_arrr = np.empty(shape=0)

    for density_shuttle in np.linspace(40,60,30):
        for coef_drag in np.linspace(0.7,0.9,30):
            loss = calError(getExperimental(),getPred(coef_drag=coef_drag,diameter=0.06,density_shuttle=density_shuttle))
            lossArray = np.append(lossArray,[loss])
            density_shuttle_arr = np.append(density_shuttle_arr,[density_shuttle])
            coef_drag_arrr = np.append(coef_drag_arrr,[coef_drag])
    print(lossArray)
    print(density_shuttle_arr)
    print(coef_drag_arrr)
    index = np.argmin(lossArray)
    print(index)
    print("Min density is", density_shuttle_arr[index],"and min coef drag is",coef_drag_arrr[index])
    # loss = calError(getExperimental(),getPred(0.6,0.06,20))
    # print(loss)
    


main()