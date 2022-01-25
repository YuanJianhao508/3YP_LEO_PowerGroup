from EnergySystem import EnergySystem
from tqdm import tqdm
import numpy as np

def basic_simulation__visualization(load,solar,storage):
    LEO = EnergySystem(load,solar,storage)
    net_profile = LEO.simulate()
    LEO.visualize(net_profile)
    return net_profile

def grid_search_2d(solar_search,storage_search_power,load=True):
    #Assume storage parameters (power/energy) are one-to-one mapped(3)
    metric_lis = []
    setting = []
    for solar in tqdm(solar_search, desc="In Progress:"):
        for stoage_power in storage_search_power:
            LEO = EnergySystem(load, [solar], [[stoage_power, stoage_power * 3]])
            net_profile = LEO.simulate()
            energy_metric = sum(net_profile * 0.5)
            metric_lis.append(energy_metric)
            setting.append([solar, stoage_power])

    m = np.array(metric_lis)
    s = np.array(setting)
    return m,s