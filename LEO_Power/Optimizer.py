from EnergySystem import EnergySystem
from tqdm import tqdm
import numpy as np
import utils

def grid_search_2d(solar_search,storage_search_power,load=True,duration=1):
    #Assume storage parameters (power/energy) are one-to-one mapped(3)
    #Hard to determine range/ exponetial increase in complexity
    np_lis = []
    for solar in tqdm(solar_search, desc="In Progress:"):
        row_lis= []
        for storage_power in storage_search_power:
            leo = EnergySystem(load, [{'size':solar,'type':'solar'}], [[storage_power, storage_power * 4]],duration)
            net_profile = leo.simulate()
            row_lis.append(net_profile)
        np_lis.append(row_lis)
    np_lis = np.array(np_lis)
    return np_lis

def gradient_ascent():
    # inputs solar size, wind size, storage power/energy size
    max_iter = 2
    n = 0
    eta = 0.1
    solar_range = [0,20]
    wind_range = [0,20]
    storage_power_range = [0,50]
    storgae_energy_range = [0,200]
    # mean normalization
    # solar = 10/(solar_range[1]-solar_range[0])
    # wind = 10/(wind_range[1]-wind_range[0])
    # generation = [{'size': solar,'type':'solar'},{'size': wind,'type':'wind'}]
    # storage_power = 20/(storage_power_range[0]-storage_power_range[1])
    # storage_energy = 50/(storgae_energy_range[0]-storgae_energy_range[1])
    solar = 10
    wind = 10
    generation = [{'size': solar,'type':'solar'},{'size': wind,'type':'wind'}]
    storage_power = 20
    storage_energy = 50
    step = 1

    while n < max_iter:
        LEO = EnergySystem(True,generation,[[storage_power,storage_energy]])
        metric = LEO.simulate('metric')


        # grad
        generation_sp = [{'size': solar+step,'type':'solar'},{'size': wind,'type':'wind'}]
        generation_wp = [{'size': solar,'type':'solar'},{'size': wind+step,'type':'wind'}]
        storage_power_p = storage_power+step
        storage_energy_p = storage_energy + step

        #update
        # solar
        sys = EnergySystem(True,generation_sp,[[storage_power,storage_energy]])
        metric_p = sys.simulate('metric')
        grad = (metric_p-metric)/step
        solar = solar - eta*grad

        # wind
        sys = EnergySystem(True,generation_wp,[[storage_power,storage_energy]])
        metric_p = sys.simulate('metric')
        grad = (metric_p-metric)/step
        wind = wind - eta*grad

        #storage_power
        sys = EnergySystem(True,generation,[[storage_power_p,storage_energy]])
        metric_p = sys.simulate('metric')
        grad = (metric_p-metric)/step
        storage_power = storage_power - eta*grad

        #storage_energy
        sys = EnergySystem(True,generation,[[storage_power,storage_energy_p]])
        metric_p = sys.simulate('metric')
        grad = (metric_p-metric)/step
        storage_energy = storage_energy - eta*grad

        n = n + 1
        print(solar,wind)

    generation = [{'size': solar,'type':'solar'},{'size': wind,'type':'wind'}]
    return generation,storage_power,storage_energy




























