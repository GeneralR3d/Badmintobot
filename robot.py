import numpy as np
import pandas as pd

modelX= pd.read_excel("output/predicted_trajectoriesX.xlsx")["LocationX"]
modelY= pd.read_excel("output/predicted_trajectoriesY.xlsx")["LocationY"]
modelZ= pd.read_excel("output/predicted_trajectoriesZ.xlsx")["LocationZ"]

passedTop = False
