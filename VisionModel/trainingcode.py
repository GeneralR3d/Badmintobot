import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import pickle

'''Trajectory 1 is left out of training dataset to be used as testing'''
data = pd.read_excel("datasetFilled3D.xlsx")

def main():
    with open('models/trained_modelX.pkl', 'wb') as file:
        gbm=train("LocationX")
        pickle.dump(gbm, file)
    with open('models/trained_modelY.pkl', 'wb') as file:
        gbm=train("LocationY")
        pickle.dump(gbm, file)
    with open('models/trained_modelZ.pkl', 'wb') as file:
        gbm=train("LocationZ")
        pickle.dump(gbm, file)
    

#swap the X and Y so that
# X is refering to lengthwise
# Y is referring to widthwise

#NOTE THE UNITS, EVERY THING IS IN MM, ANGLES ARE IN DEGREES, INITIALV IS IN M/S
#newIndex= ["time",	"LocationY","LocationX","LocationZ","LaunchY",	"LaunchX","LaunchZ","LaunchAngle",	"LaunchDirection",	"InitialV",	"label"]
#data=data.reindex(columns=newIndex)
#note that the point of origin is defined at the players side NOT THE ROBOT side
#-ve X is not possible as it is out of court + since shuttle travels from player side to robot side in ALL shots, the X-coordinate is always increasing
# +ve Y is defined as player right, robot left
# -ve Y is defined as player left, robot right

def train(output_col):
    X = data[["time", "LaunchX", "LaunchY", "LaunchZ", "LaunchAngle", "LaunchDirection", "InitialV"]]
    y = data[output_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    gbm = GradientBoostingRegressor(n_estimators=300, learning_rate=0.1, random_state=42, max_depth=50, max_features='sqrt')
    gbm.fit(X_train, y_train)
    return gbm


if __name__=="__main__":
    main()