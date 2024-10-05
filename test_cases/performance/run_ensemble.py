from sloping_slab import run_model
import sys
sys.path.append('/Users/ben/Documents/GitHub/reservoir_test_cases/test_cases/performance')
from generate_reservoirs import generate_reservoirs
import parflow as pf
import numpy as np

reservoir_amounts = [0,1,10,100,1000,10000]

# Generate the slope files
slope_x = np.ones([2,1000,1000])*.01
slope_y = np.ones([2,1000,1000])*0
pf.write_pfb("input_files/slope_x.pfb", slope_x)
pf.write_pfb("input_files/slope_y.pfb", slope_y)
generate_reservoirs()

reservoir_condition = "releasing"
rain_condition = "no_rain"
for number_of_reservoirs in reservoir_amounts:
    run_model(number_of_reservoirs, rain_condition=rain_condition, reservoir_condition=reservoir_condition)

reservoir_condition = "not_releasing"
rain_condition = "constant_rain"
for number_of_reservoirs in reservoir_amounts:
    run_model(number_of_reservoirs, rain_condition=rain_condition, reservoir_condition=reservoir_condition)


reservoir_condition = "releasing"
rain_condition = "periodic_rainfall"
for number_of_reservoirs in reservoir_amounts:
    run_model(number_of_reservoirs, rain_condition=rain_condition, reservoir_condition=reservoir_condition)
