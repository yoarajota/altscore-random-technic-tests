from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse
import random
import math
from scipy.interpolate import interp1d
import numpy as np

app = FastAPI()

T = 300  # temperature 

P_MIN = 0.05
P_MAX = 10

# present data
V_LIQUID_MIN = 0.00105
V_VAPOR_MIN = 30

# critic point
V_LIQUID_MAX = 0.0035
V_VAPOR_MAX = 0.0035

p_points = np.array([P_MIN, P_MAX])
v_liquid_points = np.array([V_LIQUID_MIN, V_LIQUID_MAX])
v_vapor_points = np.array([V_VAPOR_MIN, V_VAPOR_MAX])

# linear interpolation for liquid
liquid_interp = interp1d(p_points, v_liquid_points, kind='linear')

# log interpolation for vapor
log_v_vapor_points = np.log10(v_vapor_points)
vapor_log_interp = interp1d(p_points, log_v_vapor_points, kind='linear')

@app.get("/phase-change-diagram")
async def get_status(pressure):
    pressure = float(pressure)

    if pressure <= P_MIN:
        specific_volume_liquid = V_LIQUID_MIN
        specific_volume_vapor = V_VAPOR_MIN
    elif pressure >= P_MAX:
        specific_volume_liquid = V_LIQUID_MAX
        specific_volume_vapor = V_VAPOR_MAX
    else:
        specific_volume_liquid = float(liquid_interp(pressure))
        specific_volume_vapor = float(10 ** vapor_log_interp(pressure))
    
    return { "specific_volume_liquid": specific_volume_liquid, "specific_volume_vapor": specific_volume_vapor }