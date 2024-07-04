from Shuttle import Shuttle
import pandas as pd
import numpy as np

optimal_coef_drag = 0.598680736
optimal_diameter = 0.067522399
optimal_density_shuttle=131.8516592

shuttle = Shuttle((1/30),0.77,optimal_coef_drag,optimal_diameter,optimal_density_shuttle)
pred = shuttle.fly()[["time","y","z"]]
print(pred)
pred.to_excel("LOL.xlsx")