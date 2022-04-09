import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from GenerationAsset import GenerationAsset
from Demand import Demand
from StorageAsset import StorageAsset
from Market import Market
from tqdm import tqdm

class EnergySystem():
    def __init__(self,demand,solar,storage,simulation_duration=1):
        self.load = demand
        self.solar = solar
        self.dispatchable = storage
        self.simulation_duration = simulation_duration
        self.generation_profile = []
        self.storage_profile = []
        self.load_profile = []
        self.net_load_profile = []
        self.sample_time = []

    def simulate(self,info_select='net_load'):

        # detailed info
        generation_profile_lis = []
        load_profile_lis = []
        storage_profile_lis = []

        # load profile
        for i in self.solar:
            if i['type'] == 'solarPVT':
                PVTcapacity = i['size']
            else:
                PVTcapacity = 0

        load = Demand(self.simulation_duration)
        load_profile = load.load_profile()
        load_profile_lis.append({'load':[1],'profile':load_profile})
        print('load', sum(load_profile['Energy']))

        # generation profile
        tempdp = load.load_profile()
        net_nondispatchable_load = tempdp['Energy']
        for i, k in enumerate(self.solar):
            generation = GenerationAsset(k['size'],self.simulation_duration,k['type'])
            generation_profile = generation.load_profile()
            generation_profile_lis.append({'type-size':[k['type'],k['size']],'profile':generation_profile})
            net_nondispatchable_load -= generation_profile['Energy']
            print(k['type'], sum(generation.load_profile()['Energy']))

        #dispatchable -- battery
        # positive net_nondispatchable_load means exist load, energy need
        for i in self.dispatchable:
            storage = StorageAsset(net_nondispatchable_load, i[0], i[1],i[2])
            storage_profile = storage.get_smart_output()
            net_nondispatchable_load = net_nondispatchable_load - storage_profile
            storage_profile_lis.append({'capacity:power/energy':[i[0],i[1]],'profile':storage_profile,'type':i[2]})
            print('storage',[i[0],i[1]], sum(storage_profile))
        #Market Simulation
        market = Market(net_nondispatchable_load,load_profile_lis,generation_profile_lis,storage_profile_lis,self.solar,self.dispatchable,self.simulation_duration)
        metric = market.integrated_financial_cost()
        print('System Cost', metric)
        self.generation_profile = generation_profile_lis
        self.storage_profile = storage_profile_lis
        self.load_profile = load_profile_lis
        self.net_load_profile = net_nondispatchable_load

        if info_select == 'net_load':
            return net_nondispatchable_load
        elif info_select == 'metric':
            return metric
        elif info_select == 'load_cost':
            return net_nondispatchable_load, metric
        elif info_select == 'all_detail':
            return net_nondispatchable_load,load_profile_lis,generation_profile_lis,storage_profile_lis,metric




