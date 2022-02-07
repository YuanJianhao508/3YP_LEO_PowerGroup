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

def gradient_ascent(solar_ini,wind_ini,storage_power_ini,storage_energy_ini,solar_range,wind_range,storage_power_range,storage_energy_range,info='final'):
    # inputs solar size, wind size, storage power/energy size
    max_iter = 100
    n = 0
    eta = 0.00001
    duration = 3
    # mean normalization
    # solar = 10/(solar_range[1]-solar_range[0])
    # wind = 10/(wind_range[1]-wind_range[0])
    # generation = [{'size': solar,'type':'solar'},{'size': wind,'type':'wind'}]
    # storage_power = 20/(storage_power_range[0]-storage_power_range[1])
    # storage_energy = 50/(storgae_energy_range[0]-storgae_energy_range[1])
    solar = solar_ini
    wind = wind_ini
    generation = [{'size': solar,'type':'solar'},{'size': wind,'type':'wind'}]
    storage_power = storage_power_ini
    storage_energy = storage_energy_ini
    step = 1
    metric = -99999999999

    solar_lis = []
    wind_lis = []
    storage_plis = []
    storage_elis = []
    metric_lis = []

    while n < max_iter and solar != 0:

        LEO = EnergySystem(True,generation,[[storage_power,storage_energy]],duration)
        metric = LEO.simulate('metric')


        # grad
        generation_sp = [{'size': solar+step,'type':'solar'},{'size': wind,'type':'wind'}]
        generation_wp = [{'size': solar,'type':'solar'},{'size': wind+step,'type':'wind'}]
        storage_power_p = storage_power+step
        storage_energy_p = storage_energy + step

        #update
        # solar
        sys = EnergySystem(True,generation_sp,[[storage_power,storage_energy]],duration)
        metric_p = sys.simulate('metric')
        grad = (metric_p-metric)/step
        solar = solar + eta*grad

        # wind
        sys = EnergySystem(True,generation_wp,[[storage_power,storage_energy]],duration)
        metric_p = sys.simulate('metric')
        grad = (metric_p-metric)/step
        wind = wind + eta*grad

        #storage_power
        sys = EnergySystem(True,generation,[[storage_power_p,storage_energy]],duration)
        metric_p = sys.simulate('metric')
        grad = (metric_p-metric)/step
        storage_power = storage_power + eta*grad

        #storage_energy
        sys = EnergySystem(True,generation,[[storage_power,storage_energy_p]],duration)
        metric_p = sys.simulate('metric')
        grad = (metric_p-metric)/step
        storage_energy = storage_energy + eta*grad

        solar = min(solar_range[1],solar)
        solar = max(solar_range[0], solar)
        wind = min(wind_range[1], wind)
        wind = max(wind_range[0], wind)
        storage_power = min(storage_power_range[1],storage_power)
        storage_power = max(storage_power_range[0], storage_power)
        storage_energy = min(storage_energy_range[1],storage_energy)
        storage_energy = max(storage_energy_range[0], storage_energy)

        solar_lis.append(solar)
        wind_lis.append(wind)
        storage_plis.append(storage_power)
        storage_elis.append(storage_energy)
        metric_lis.append(metric)
        n = n + 1
        print('current setting', solar, wind, storage_power, storage_energy,metric)


    generation = [{'size': solar,'type':'solar'},{'size': wind,'type':'wind'}]
    if info == 'list':
        return solar_lis,wind_lis,storage_plis,storage_elis,metric_lis
    else:
        return generation,storage_power,storage_energy,metric

def random_ga(solar_range,wind_range,storage_power_range,storage_energy_range):
    nsample = 100
    step = 1
    sr = np.arange(solar_range[0],solar_range[1],step)
    wr = np.arange(wind_range[0],wind_range[1],step)
    spr = np.arange(storage_power_range[0],storage_power_range[1],step)
    ser = np.arange(storage_energy_range[0],storage_energy_range[1],step)
    solar_rand = np.random.choice(sr, nsample)
    wind_rand = np.random.choice(wr, nsample)
    sp_rand = np.random.choice(spr, nsample)
    se_rand = np.random.choice(ser, nsample)

    res = []
    metric_lis = []
    for i in tqdm(range(len(solar_rand))):
        print('iteration:',i)
        [generation,storage_power,storage_energy,metric] = gradient_ascent(solar_rand[i], wind_rand[i], sp_rand[i], se_rand[i], solar_range, wind_range,
                        storage_power_range, storage_energy_range)
        res.append([generation,storage_power,storage_energy])
        metric_lis.append(metric)

    index = np.array(metric_lis).argmax()
    best_res = res[index]
    return best_res





























