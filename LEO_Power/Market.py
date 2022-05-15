import pandas as pd
import numpy as np


class Market():
    def __init__(self,net_nondispatchable_load,load_profile_lis,generation_profile_lis,storage_profile_lis,generation,storage,duration):
        self.solar_profile = generation_profile_lis
        self.storage_profile = storage_profile_lis
        self.load_profile = load_profile_lis
        self.net_load_profile = net_nondispatchable_load[:-1]
        self.generation = generation
        self.storage = storage
        # simulation duration consider it in NPV
        self.duration = duration
        self.price = pd.read_csv('./Data/price.csv')
        self.pimp_lis = np.array(self.price['pimp'])
        self.pexp_lis = np.array(self.price['pexp'])


    def integrated_financial_cost(self,rhc=True):
            return self.running_cost(rhc)+self.installation_cost()

    def running_cost(self,rhc):
        if rhc:
            running_cost = self.pimp_lis @ np.maximum(self.net_load_profile, 0) - self.pexp_lis @ np.minimum(self.net_load_profile, 0)
        else:
            posnp = sum(np.maximum(self.net_load_profile, 0))
            negnp = sum(np.minimum(self.net_load_profile, 0))
            financial_cost = negnp * 65 + posnp * 150
            carbon_cost = posnp * 159
            running_cost = financial_cost + carbon_cost
        return running_cost

    def installation_cost(self):
        install_cost = 0
        for i in self.generation:
            if i['type'] == 'solar':
                install_cost += (11500+6400) * self.duration * i['size']
            if i['type'] == 'solarPVT':
                install_cost += (11500+6400) * self.duration * i['size']
            elif i['type'] == 'wind':
                install_cost += (23500+40320)/2 * self.duration * i['size']

        for i in self.storage:
            if i[2] == 'local':
                install_cost += 20000 * self.duration * i[1] + 2000 * self.duration * i[0]
            elif i[2] == 'hydrogen':
                install_cost += (10000+20000) * self.duration * i[1] + 5000 * self.duration * i[0]
        return install_cost

    def tariff(self):
        pass

    def see_state(self):
        print(self.net_load_profile)
        print(self.load_profile)
        print(self.solar_profile)
        print(self.storage_profile)
        print(self.generation)
        print(self.storage)

