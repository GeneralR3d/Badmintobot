import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import pickle

data = pd.read_excel("dataset3.xlsx")
X = data[["time", "LaunchX", "LaunchY", "LaunchZ", "LaunchAngle", "LaunchDirection", "InitialV"]]
y = data[["LocationX","LocationY","LocationZ"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
gbm = GradientBoostingRegressor(n_estimators=300, learning_rate=0.1, random_state=42, max_depth=50, max_features='sqrt')
gbm.fit(X_train, y_train)

with open('trained_model.pkl', 'wb') as file:
    pickle.dump(gbm, file)
