import pandas as pd
import numpy as np
from darts import TimeSeries
from darts.models import XGBModel

'''Trajectory 1 is left out of training dataset to be used as testing'''
data = pd.read_excel("../preprocessing/datasetFilledDynamicStaticFeatures.xlsx")
data.rename(columns={'time':'frame'},inplace=True)
for labelNo in data['label'].unique():
    currentDF=data[data['label']==labelNo]
    frames = pd.Series(np.arange(0,len(currentDF)))
    frames.index = currentDF.index
    currentDF['frame'] = frames
    data.update(currentDF)


seriesOfTrajectories = [
    TimeSeries.from_dataframe(
        df=data[data['label']==labelNo],
        static_covariates=((data[data['label']==labelNo])[['LaunchX','LaunchY','LaunchZ','LaunchAngle','LaunchDirection','InitialV']]).head(1)
    ) 
    for labelNo in data['label'].unique()
    ]
# seriesOfTrajectories = TimeSeries.from_group_dataframe(
#     df=data,
#     group_cols= 'label',
#     static_cols=["LaunchX", "LaunchY", "LaunchZ", "LaunchAngle", "LaunchDirection", "InitialV"]
# )
# seriesOfTrajectories = [traj.drop_columns('label') for traj in seriesOfTrajectories]
print(seriesOfTrajectories[0].static_covariates)
print(seriesOfTrajectories[0].static_covariates_values)

targets = [TimeSeries[['LocationX','LocationY','LocationZ']] for TimeSeries in seriesOfTrajectories]
pastCov = [TimeSeries[['diffX','diffY','diffZ','diffAngle','diffDirection','vDiff']] for TimeSeries in seriesOfTrajectories]
gbm = XGBModel(lags=5,output_chunk_length=40,lags_past_covariates=5,use_static_covariates=True)
gbm.fit(series=targets,past_covariates=pastCov)
gbm.save('../models/trained_model_darts.pkl')




# def main():



# def train():
#     X = data[["time", "LaunchX", "LaunchY", "LaunchZ", "LaunchAngle", "LaunchDirection", "InitialV"]]
#     y = data[["LocationX","LocationY","LocationZ"]]
#     #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#     params = {'n_estimators': 300, 
#               'learning_rate':0.1,
#               'random_state':42,  
#               'max_depth':50,  
#               'max_features': 'sqrt'}
#     gbm = MultiOutputRegressor(GradientBoostingRegressor(**params))
#     gbm.fit(X,y)
#     return gbm


# if __name__=="__main__":
#     main()