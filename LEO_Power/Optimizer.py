from EnergySystem import EnergySystem
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

def grid_search_2d(solar_search,storage_search_power,load=True,duration=1):
    #Assume storage parameters (power/energy) are one-to-one mapped(3)
    #Hard to determine range/ exponetial increase in complexity
    np_lis = []
    for solar in tqdm(solar_search, desc="In Progress:"):
        row_lis= []
        for stoage_power in storage_search_power:
            leo = EnergySystem(load, [solar], [[stoage_power, stoage_power * 3]],duration)
            net_profile = leo.simulate()
            row_lis.append(net_profile)
        np_lis.append(row_lis)
    np_lis = np.array(np_lis)
    return np_lis

def SGD():
    pass



