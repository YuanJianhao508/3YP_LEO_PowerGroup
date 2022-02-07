import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from GenerationAsset import GenerationAsset
from Load import Load
from StorageAsset import StorageAsset
from Market import Market
from tqdm import tqdm

class EnergySystem():
    def __init__(self,load,solar,storage,simulation_duration=1):
        self.load = load
        self.solar = solar
        self.dispatchable = storage
        self.simulation_duration = simulation_duration

    def simulate(self,info_select='net_load'):

        # detailed info
        generation_profile_lis = []
        load_profile_lis = []
        storage_profile_lis = []

        # load profile
        load = Load(self.simulation_duration)
        load_profile = load.load_profile()
        load_profile_lis.append({'load':[1],'profile':load_profile})

        # solar profile
        for i, k in enumerate(self.solar):
            generation = GenerationAsset(k['size'],self.simulation_duration,k['type'])
            if i == 0:
                generation_profile = generation.load_profile()
            else:
                generation_profile += generation.load_profile()


            generation_profile_lis.append({'type-size':[k['type'],k['size']],'profile':generation_profile})

        #dispatchable -- battery
        net_nondispatchable_load = load_profile['Energy'] - generation_profile['Energy']
        for i in self.dispatchable:
            storage = StorageAsset(net_nondispatchable_load, i[0], i[1])
            storage_profile = storage.get_output()
            net_nondispatchable_load = net_nondispatchable_load - storage_profile
            storage_profile_lis.append({'capacity:power/energy':[i[0],i[1]],'profile':storage_profile})

        #Market Simulation
        market = Market(net_nondispatchable_load,load_profile_lis,generation_profile_lis,storage_profile_lis,self.solar,self.dispatchable,self.simulation_duration)
        metric = market.integrated_financial_cost()

        if info_select == 'net_load':
            return net_nondispatchable_load
        elif info_select == 'metric':
            return metric
        elif info_select == 'load_cost':
            return net_nondispatchable_load, metric
        elif info_select == 'all_detail':
            return net_nondispatchable_load,load_profile_lis,generation_profile_lis,storage_profile_lis,metric

    def visualize(self,net_nondispatchable_load):
        plt.plot(net_nondispatchable_load)
        plt.xlabel('Time Step')
        plt.ylabel('Net Load (Energy Level)')
        plt.title('Simulation Sample Data')
        plt.show()


if __name__ == 'main':
    solar_farm = GenerationAsset(30,duration=1,type='solar')
    solar_panel = GenerationAsset(17.5,duration=1,type='solar')

    solar_profile = solar_farm.load_profile()+solar_panel.load_profile()

    # get demand profile
    load = Load()
    load_profile = load.load_profile()


    #get ned load and feed to storage
    net_nondispatchable_load = load_profile['Energy'] - solar_profile['Energy']


    #get storage output
    local_battery = StorageAsset(net_nondispatchable_load,7.5,20)
    local_battery_profile = local_battery.get_output()

    net_nondispatchable_load = net_nondispatchable_load - local_battery_profile
    hydrogen = StorageAsset(net_nondispatchable_load,7.5,20)
    hydrogen_profile = hydrogen.get_output()
    net_nondispatchable_load = net_nondispatchable_load - hydrogen_profile

    #visualize
    plt.plot(net_nondispatchable_load)
    plt.xlabel('Time Step')
    plt.ylabel('Net Load (Energy Level)')
    plt.title('Simulation Sample Data')
    # plt.savefig('e4.png')
    plt.show()

