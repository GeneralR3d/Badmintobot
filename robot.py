import numpy as np
import pandas as pd
import math

modelX= pd.read_excel("output/predicted_trajectoriesX.xlsx")
modelY= pd.read_excel("output/predicted_trajectoriesY.xlsx")
modelZ= pd.read_excel("output/predicted_trajectoriesZ.xlsx")

def main():
    CONTACT_Z = 1300
    LENGTH_OF_RACKET = 630
    HEIGHT_OF_ROBOT = 500
    targetPoint = (13400,-5640,0.0) #put 3D even though we assume Z-coordinate of landing point to forever be 0
    DURATION_OF_SWING = 0.0

    timeOfContact = getTimeFromZ(CONTACT_Z)
    # pointOfContact= getXAtTime(timeOfContact), getYAtTime(timeOfContact), CONTACT_Z
    pointOfContact = 1000,-1000,1300

    launchAngle= math.sin((CONTACT_Z-HEIGHT_OF_ROBOT)/(LENGTH_OF_RACKET))
    launchDirection= math.tan((targetPoint[1]-pointOfContact[1])/(targetPoint[0]-pointOfContact[0]))

    ROBOT_X = (LENGTH_OF_RACKET* math.cos(launchAngle) * math.cos(launchDirection)) + pointOfContact[0]
    ROBOT_Y = (LENGTH_OF_RACKET* math.cos(launchAngle) * math.sin(launchDirection)) + pointOfContact[1]

    robotPoint= (ROBOT_X,ROBOT_Y,0.0)
    timeStartSwing = timeOfContact - DURATION_OF_SWING

    print(f"Point of contact is {pointOfContact}")
    print(f"Robot coordinates are {robotPoint}")
    print(f"Launch Direction in degree is {launchDirection * (180/math.pi)}")
    print(f"Time to start swinging is {timeStartSwing}")



def getTimeFromZ(contactHeight = 1300):
    CONTACT_Z = contactHeight
    MAX_HEIGHT= modelZ["LocationZ"].max()
    passedMaxHeight = False


    #using for loop is important as the sequence of these numbers matter, need to start at the top which is at time=0s
    for i in range(modelZ["LocationZ"].size):
        if not passedMaxHeight and abs(modelZ["LocationZ"][i] - MAX_HEIGHT) < 1e-9 :
            passedMaxHeight=True
        if passedMaxHeight:
            if modelZ["LocationZ"][i] == CONTACT_Z:
                #print(f'Time is {modelZ["time"][i]}')
                return modelZ["time"][i]
            elif modelZ["LocationZ"][i] < CONTACT_Z:
                heightBelow = modelZ["LocationZ"][i]
                heightAbove = modelZ["LocationZ"][i-1]
                result = (((modelZ["time"][i]- modelZ["time"][i-1])*(CONTACT_Z - heightAbove))/(heightBelow-heightAbove)) + (modelZ["time"][i-1])
                #print(f"Time is {result}")
                return result
        
        
def getXAtTime(timeOfContact):
    
    for i in range(modelX["LocationX"].size):
        if modelX["time"][i] == timeOfContact:
           #print(f'Point of contact X is {modelX["LocationX"][i]}')
           return modelX["LocationX"][i]
        elif modelX["time"][i] > timeOfContact:
           timeBefore = modelX["time"][i-1]
           timeAfter = modelX["time"][i]
           result = (((modelX["LocationX"][i]- modelX["LocationX"][i-1])*(timeOfContact-timeBefore))/(timeAfter-timeBefore)) + modelX["LocationX"][i-1]
           #print(f"Point of contact X is {result}")
           return result
    
def getYAtTime(timeOfContact):
    
    for i in range(modelY["LocationY"].size):
        if modelX["time"][i] == timeOfContact:
           #print(f'Point of contact Y is {modelY["LocationY"][i]}')
           return modelY["LocationY"][i]
        elif modelY["time"][i] > timeOfContact:
           timeBefore = modelY["time"][i-1]
           timeAfter = modelY["time"][i]
           result = (((modelY["LocationY"][i]- modelY["LocationY"][i-1])*(timeOfContact-timeBefore))/(timeAfter-timeBefore)) + modelY["LocationY"][i-1]
           #print(f'Point of contact Y is {result}')
           return result
    

if __name__ == "__main__":
    main()