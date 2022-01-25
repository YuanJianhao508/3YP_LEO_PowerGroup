import Optimisation as op
import numpy as np

# Basic simulation
# solar = [30,17.5]
# load = True
# storage = [[7.5,20],[7.5,20]]
# net_profile = op.basic_simulation__visualization(load,solar,storage)

#grid search 2d test
solar_search = list(range(35, 35 + 50, 1))
storage_search_power = list(range(10, 10 + 50, 1))
[m,s] = op.grid_search_2d(solar_search,storage_search_power,load=True)
np.save('Result/2d_search_metric_test1.npy', m)
np.save('Result/2d_search_setting_test1.npy', s)