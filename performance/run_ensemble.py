from sloping_slab import run_model

reservoir_amounts = [0,1,10,100,1000,10000]

# reservoir_configurations = [0]

# filling case
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
