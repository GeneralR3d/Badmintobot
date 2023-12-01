import pandas as pd
import numpy as np
import pickle
import math
import time

class PredictClass:
    """
    This idea does not work. our desired ouput Y we want is of length 61 but our input of 6 frames means each of our partial input feature arrays are of the wrong length and would not work.
    Need to introduce lag features.
    """

    TIME_INTERVAL = 1/30
    end_time = None
    time_points = None
    launchX= None
    launchY= None
    launchZ= None
    diffX= None
    diffY= None
    diffZ= None

    def __init__(self,end_time,input_frames):
        self.end_time = end_time
        self.time_points = np.arange(0, end_time + self.TIME_INTERVAL, self.TIME_INTERVAL)

        dataset = pd.read_excel("../../testData/Vision Trajectory3.xlsx",'Trajectory 1')
        correctedDF = pd.DataFrame()
        correctedDF["LocationX"] = dataset["y"] *10
        correctedDF["LocationY"] = dataset["x"] *10
        correctedDF["LocationZ"] = dataset["z"] *10

        self.launchX= correctedDF["LocationX"][0:input_frames]
        self.launchY= correctedDF["LocationY"][0:input_frames]
        self.launchZ= correctedDF["LocationZ"][0:input_frames]

        self.diffX= pd.Series([j-i for i,j in zip(self.launchX, self.launchX[1:])])
        self.diffY= pd.Series([j-i for i,j in zip(self.launchY, self.launchY[1:])])
        self.diffZ= pd.Series([j-i for i,j in zip(self.launchZ, self.launchZ[1:])])

    def predict(self):

        predictStartTime = time.time()
        print(self.launchX)
        print(self.launchY)
        print(self.launchZ)

        # Load the trained model
        with open('../models/trained_model_Dynamic.pkl', 'rb') as file:
            pickleStartTime = time.time()
            gbm = pickle.load(file)
            print(f"Pickle loading takes {time.time()-pickleStartTime}sec")
            pred_gbm=self.predictData(gbm)

            # Output the predicted data
            predicted_data = pd.DataFrame({
                "time": self.time_points,
                "LocationX": pred_gbm[0],
                "LocationY": pred_gbm[1],
                "LocationZ": pred_gbm[2]
            })
            toExcel = time.time()
            predicted_data.to_excel("output/predicted_trajectoriesCombined.xlsx", index=False)
            print(f"Saving to excel takes {time.time()-toExcel} sec")



        print(f"Whole prediction takes { time.time() - predictStartTime}sec")


    
    def predictData(self,gbm):
        predictStart = time.time()

        input_data = pd.DataFrame({
            "time": None,    
            "diffX": self.diffX, #note these can be swapped cos in the trained model X is wrt to court
            "diffY": self.diffY,
            "diffZ": self.diffZ,
            "diffAngle": pd.Series([math.atan((self.diffZ[i])/(math.sqrt(self.diffX[i]**2 + self.diffY[i]**2))) * (180/math.pi) for i in range(len(self.diffX))]),
            #calculate from arctan(opp/adj) which is arctan(diffZ/change in xandy) which is arctan(diffZ/sqrt(diffX^2 + diffY^2))
            #essentially calculated from a rotation around the y-axis
            "diffDirection": pd.Series([(math.atan((self.diffY[i])/(math.sqrt(self.diffX[i]**2 + self.diffZ[i]**2))) * (180/math.pi)) for i in range(len(self.diffX))]),
                #calculate from arctan(opp/adj) which is arctan(change in x/change in yandz) which is arctan( diffX/sqrt(diffY^2 + diffZ^2)
                #calculated from a rotation around the z-axis
            "vDiff": pd.Series([(math.sqrt(self.diffX[i]**2 + self.diffY[i]**2 + self.diffZ[i]**2)/self.TIME_INTERVAL)/1000 for i in range(len(self.diffX))])

                #calcuate from change in the 3d position over change in time period
                #recall velocity is a vector so the initialV can only be length of that vector
                #vector is a difference in all 3 coordinates
        })
        y_pred_gbm = gbm.predict(input_data)
        y_pred_gbm = y_pred_gbm.transpose()
        
        print(f"Model predict takes {time.time()- predictStart}sec")
        return y_pred_gbm
    
    def findStart(self,dataframe):
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
                                    (nextRow['LocationZ'] - row['LocationZ'])**2)) /(self.TIME_INTERVAL)
            speeds.append((forwardSpeed,i,i+1))
        speeds.sort(key= lambda x:x[0],reverse=True)
        trueStartIndex = speeds[0][2]
        return dataframe[trueStartIndex:]
    

if __name__ == "__main__":
    prediction = PredictClass(2,6)
    prediction.predict()