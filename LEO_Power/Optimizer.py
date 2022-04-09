from EnergySystem import EnergySystem
from tqdm import tqdm
import numpy as np
import copy
import statistics
import utils

def GridSearch(solar_search,wind_search,storage_search):
    net_loads = np.zeros((len(solar_search),len(wind_search),len(storage_search)))
    net_costs = np.zeros((len(solar_search),len(wind_search),len(storage_search)))
    for i,solar in enumerate(tqdm(solar_search)):
        for j,wind in enumerate(wind_search):
            for k,storage in enumerate(storage_search):
                leo = EnergySystem(3500, [{'size': solar, 'type': 'solar'},{'size': wind, 'type': 'wind'}], [[storage, storage * 10,'local']])
                net_load, metric = leo.simulate('load_cost')
                net_loads[i,j,k] = 1
                net_costs[i,j,k] = metric
    return net_loads,net_costs


def SGD(theta,batch_size=1,duration=1):
    generation,storage = theta[0],theta[1]
    gen_clip = {'solar':100,'wind':5}

    max_iter = 100
    epoch = 0
    step = 0.001
    eta = 0.0001
    log = []
    g_log= []
    s_log = []
    while epoch < max_iter:
        LEO = EnergySystem(3500, generation,storage, duration)
        metric_lis = []
        for batch in range(batch_size):
            m = LEO.simulate('metric')
            metric_lis.append(m)
        metric = statistics.mean(metric_lis)
        log.append(metric)
        # calculate grad
        updateg = copy.deepcopy(generation)
        tempg = copy.deepcopy(generation)
        for gen in range(len(generation)):
            tempg[gen]['size'] = tempg[gen]['size']+step
            # print(tempg)
            sys = EnergySystem(3500, tempg, storage, duration)
            grad_lis = []
            for b in range(batch_size):
                metric_p = sys.simulate('metric')
                print(metric_p)
                g = (metric_p - metric) / step
                grad_lis.append(g)
            grad = statistics.mean(grad_lis)

            print(grad)
            updateg[gen]['size'] = min((updateg[gen]['size'] - eta * grad),gen_clip[updateg[gen]['type']])
            tempg = copy.deepcopy(generation)

        updates = copy.deepcopy(storage)
        temps = copy.deepcopy(storage)
        for s in range(len(storage)):
            for index in range(2):
                temps[s][index] = temps[s][index]+step
                # print(temps)
                sys = EnergySystem(3500, generation, temps, duration)
                grad_lis = []
                for b in range(batch_size):
                    metric_p = sys.simulate('metric')
                    g = (metric_p - metric) / step
                    grad_lis.append(g)
                grad = statistics.mean(grad_lis)
                print(grad)
                updates[s][index] = updates[s][index] - eta * grad

                temps = copy.deepcopy(storage)

        g_log.append(generation)
        s_log.append(storage)

        generation = updateg
        storage = updates

        print(generation,storage)
        epoch = epoch+1

    return g_log,s_log,log
























