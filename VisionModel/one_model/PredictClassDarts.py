import pandas as pd
import numpy as np
from darts import TimeSeries
from darts.models import XGBModel
import math
import time

class PredictClassDarts:

# we need to associate each "difference" feature, 'diffX','diffY','diffZ','diffAngle','diffDirection','vDiff' to the i+1 time stamp not i
# This means that arrow is pointing forward from first coordinate to second coordinate, but now its tagged at the second coordinate instead
# 1) If we dont do so we are actually leaking data into the "future" when doing past covariates in time series regression
# 2) It makes more sense for the first value of each "difference" feature to be 0, where 2 points havent existed to calculate the difference, than the last coordinate
# the very 1st value of each difference feature can either be 0 or NaN

    TIME_INTERVAL = 1/30
    end_time = None
    time_points = None
    length_of_snippet = None
    snippetX= None
    snippetY= None
    snippetZ= None
    diffX= None
    diffY= None
    diffZ= None

    # for static covariates
    launchX= None
    launchY= None
    launchZ= None
    changeX= None
    changeY= None
    changeZ= None

    # model constant
    OUTPUT_CHUNK_SIZE = 40

    def __init__(self,end_time,start_frame,end_frame):


        self.end_time = end_time
        self.time_points = np.arange(0, end_time + self.TIME_INTERVAL, self.TIME_INTERVAL) #TODO not used for now since not able to generate any sized prediction from model

        dataset = pd.read_excel("../../testData/Vision Trajectory3.xlsx",'Trajectory 1')
        correctedDF = pd.DataFrame()
        correctedDF["LocationX"] = dataset["y"] *10
        correctedDF["LocationY"] = dataset["x"] *10
        correctedDF["LocationZ"] = dataset["z"] *10

        if start_frame < 0 or end_frame < 0:
            raise ArithmeticError("Frame number cannot be negative!")
        if start_frame > len(correctedDF) or end_frame > len(correctedDF):
            raise IndexError("Out of range!")
        if start_frame > end_frame:
            raise ArithmeticError("Start frame cannot be after end frame!")
        if end_frame - start_frame < 1:
            raise ArithmeticError("Snippet must be at least one frame long!")
        
        self.length_of_snippet = end_frame - start_frame + 1
        

        self.snippetX= ((correctedDF["LocationX"]).iloc[start_frame: end_frame+1]).copy(deep=True).reset_index(drop=True)
        self.snippetY= ((correctedDF["LocationY"]).iloc[start_frame: end_frame+1]).copy(deep=True).reset_index(drop=True)
        self.snippetZ= ((correctedDF["LocationZ"]).iloc[start_frame: end_frame+1]).copy(deep=True).reset_index(drop=True)

        self.diffX= pd.Series([j-i for i,j in zip(self.snippetX, self.snippetX[1:])])
        self.diffY= pd.Series([j-i for i,j in zip(self.snippetY, self.snippetY[1:])])
        self.diffZ= pd.Series([j-i for i,j in zip(self.snippetZ, self.snippetZ[1:])])

        self.diffX = pd.concat([pd.Series([0]),self.diffX],ignore_index=True)
        self.diffY = pd.concat([pd.Series([0]),self.diffY],ignore_index=True)
        self.diffZ = pd.concat([pd.Series([0]),self.diffZ],ignore_index=True)

        self.launchX = self.snippetX[0]
        self.launchY = self.snippetY[0]
        self.launchZ = self.snippetZ[0]

        self.changeX = self.diffX[1]
        self.changeY = self.diffY[1]
        self.changeZ = self.diffZ[1]

    def predict(self):

        predictStartTime = time.time()

        # Load the trained model
        pickleStartTime = time.time()
        gbm = XGBModel.load('../models/trained_model_darts.pkl')
        print(f"Model loading takes {time.time()-pickleStartTime}sec")
        pred_gbm=self.predictData(gbm)

        # Output the predicted data
        predicted_data = pd.DataFrame({
            "time": np.arange(0,self.OUTPUT_CHUNK_SIZE + self.length_of_snippet) * self.TIME_INTERVAL,
            "LocationX": pd.concat([self.snippetX,pred_gbm['LocationX'].pd_series()],ignore_index=True),
            "LocationY": pd.concat([self.snippetY,pred_gbm['LocationY'].pd_series()],ignore_index=True),
            "LocationZ": pd.concat([self.snippetZ,pred_gbm['LocationZ'].pd_series()],ignore_index=True)
        })
        toExcel = time.time()
        predicted_data.to_excel("output/predicted_trajectories_DartsCombined.xlsx", index=False)
        print(f"Saving to excel takes {time.time()-toExcel} sec")



        print(f"Whole prediction takes { time.time() - predictStartTime}sec")


    
    def predictData(self,gbm):
        predictStart = time.time()
        targetDF = pd.DataFrame({
                'LocationX': self.snippetX,
                'LocationY': self.snippetY,
                'LocationZ': self.snippetZ,
                "LaunchX": self.launchX,
                "LaunchY": self.launchY,
                "LaunchZ": self.launchZ,
                "LaunchAngle": math.atan((self.changeZ)/(math.sqrt(self.changeX**2 + self.changeY**2))) * (180/math.pi),
                "LaunchDirection": (math.atan((self.changeY)/(math.sqrt(self.changeX**2 + self.changeZ**2))) * (180/math.pi)),
                "InitialV": (math.sqrt(self.changeX**2 + self.changeY**2 + self.changeZ**2)/self.TIME_INTERVAL)/1000
            })

        # target = TimeSeries.from_dataframe(
        #     pd.DataFrame({
        #         'LocationX': self.snippetX,
        #         'LocationY': self.snippetY,
        #         'LocationZ': self.snippetZ,
        #         "LaunchX": [self.launchX] *len(self.snippetX),
        #         "LaunchY": [self.launchY] *len(self.snippetX),
        #         "LaunchZ": [self.launchZ] *len(self.snippetX),
        #         "LaunchAngle": [math.atan((self.changeZ)/(math.sqrt(self.changeX**2 + self.changeY**2))) * (180/math.pi)] *len(self.snippetX),
        #         "LaunchDirection": [(math.atan((self.changeY)/(math.sqrt(self.changeX**2 + self.changeZ**2))) * (180/math.pi))] *len(self.snippetX),
        #         "InitialV": [(math.sqrt(self.changeX**2 + self.changeY**2 + self.changeZ**2)/self.TIME_INTERVAL)/1000] *len(self.snippetX)
        #     }),static_covariates=["LaunchX", "LaunchY", "LaunchZ", "LaunchAngle", "LaunchDirection", "InitialV"]
        # )
        target = TimeSeries.from_dataframe(targetDF,value_cols=['LocationX','LocationY','LocationZ'],static_covariates=(targetDF[["LaunchX", "LaunchY", "LaunchZ", "LaunchAngle", "LaunchDirection", "InitialV"]]).head(1))

        pastCov = TimeSeries.from_dataframe(
            pd.DataFrame({   
                "diffX": self.diffX, #note these can be swapped cos in the trained model X is wrt to court
                "diffY": self.diffY,
                "diffZ": self.diffZ,
                "diffAngle": pd.Series([0]+[math.atan((self.diffZ[i])/(math.sqrt(self.diffX[i]**2 + self.diffY[i]**2))) * (180/math.pi) for i in range(1,len(self.diffX))]),
                #calculate from arctan(opp/adj) which is arctan(diffZ/change in xandy) which is arctan(diffZ/sqrt(diffX^2 + diffY^2))
                #essentially calculated from a rotation around the y-axis
                "diffDirection": pd.Series([0]+[(math.atan((self.diffY[i])/(math.sqrt(self.diffX[i]**2 + self.diffZ[i]**2))) * (180/math.pi)) for i in range(1,len(self.diffX))]),
                    #calculate from arctan(opp/adj) which is arctan(change in x/change in yandz) which is arctan( diffX/sqrt(diffY^2 + diffZ^2)
                    #calculated from a rotation around the z-axis
                "vDiff": pd.Series([0]+[(math.sqrt(self.diffX[i]**2 + self.diffY[i]**2 + self.diffZ[i]**2)/self.TIME_INTERVAL)/1000 for i in range(1,len(self.diffX))])

                    #calcuate from change in the 3d position over change in time period
                    #recall velocity is a vector so the initialV can only be length of that vector
                    #vector is a difference in all 3 coordinates
                })
        )
        y_pred_gbm = gbm.predict(n=self.OUTPUT_CHUNK_SIZE,series=target,past_covariates=pastCov,verbose=True)
        #y_pred_gbm = y_pred_gbm.transpose()
        
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
    prediction = PredictClassDarts(2,2,6)
    prediction.predict()