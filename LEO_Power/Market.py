import pandas as pd
import numpy as np


class Market():
    def __init__(self,net_nondispatchable_load,load_profile_lis,generation_profile_lis,storage_profile_lis,generation,storage,duration):
        self.solar_profile = generation_profile_lis
        self.storage_profile = storage_profile_lis
        self.load_profile = load_profile_lis
        self.net_load_profile = net_nondispatchable_load
        self.generation = generation
        self.storage = storage
        # simulation duration consider it in NPV
        self.duration = duration



    def integrated_financial_cost(self):
        return self.running_cost()-self.installation_cost()

    def running_cost(self):
        posnp = sum(np.maximum(self.net_load_profile, 0))
        negnp = sum(np.minimum(self.net_load_profile, 0))
        financial_cost = negnp * 90 - posnp * 160 * 1.5
        carbon_cost = posnp * 309
        running_cost = financial_cost - carbon_cost
        return running_cost

    def installation_cost(self):
        install_cost = 0
        for i in self.generation:
            if i['type'] == 'solar':
                install_cost += 8000 * self.duration * i['size']
            elif i['type'] == 'wind':
                install_cost += 9000 * self.duration * i['size']

        for i in self.storage:
            install_cost += 12000 * self.duration * i[0]

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