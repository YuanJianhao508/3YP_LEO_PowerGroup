from EnergySystem import EnergySystem
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

def basic_simulation__visualization(load,solar,storage,full_info=True):
    LEO = EnergySystem(load,solar,storage,full_info)
    net_profile = LEO.simulate()
    LEO.visualize(net_profile)
    return net_profile

def excess_cost(net_profile):
    pass

def grid_search_2d(solar_search,storage_search_power,load=True):
    #Assume storage parameters (power/energy) are one-to-one mapped(3)
    #Hard to determine range/ exponetial increase in complexity
    setting = []
    area_lis = []
    posarea_lis = []
    np_lis = []
    for solar in tqdm(solar_search, desc="In Progress:"):
        for stoage_power in storage_search_power:
            leo = EnergySystem(load, [solar], [[stoage_power, stoage_power * 3]])
            net_profile = leo.simulate()
            np_lis.append(net_profile)
    np_lis = np.array(np_lis)
    return np_lis

def grid_search_3d(solar_search,storage_search_power,storage_search_energy,load=True):
    #Assume storage parameters (power/energy) are one-to-one mapped(3)
    metric_lis = []
    setting = []
    for solar in tqdm(solar_search, desc="In Progress:"):
        for stoage_power in storage_search_power:
            for storage_energy in storage_search_energy:
                leo = EnergySystem(load, [solar], [[stoage_power, storage_energy]])
                net_profile = leo.simulate()
                energy_metric = sum(net_profile * 0.5)
                metric_lis.append(energy_metric)
                setting.append([solar, stoage_power,storage_energy])

    m = np.array(metric_lis)
    s = np.array(setting)
    return m,s

def grid_search_analysis(m,s):
    plt.plot(list(range(len(m))),m)
    plt.xlabel('Settings Index')
    plt.ylabel('Energy excess Metric')
    plt.title('Grid search')
    plt.show()
    return s[np.argmin(m)]



