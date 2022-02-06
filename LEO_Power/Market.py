import pandas as pd
import numpy as np

class Market():
    def __init__(self,net_nondispatchable_load,load_profile_lis,generation_profile_lis,storage_profile_lis):
        self.solar_profile = generation_profile_lis
        self.storage_profile = storage_profile_lis
        self.load_profile = load_profile_lis
        self.net_load_profile = net_nondispatchable_load


    def load_info(self):

        pass

    def installation_cost(generation, storage):
        install_cost = 0
        for i in generation:
            if i['type'] == 'solar':
                install_cost += 8800 * i['size']
            elif i['type'] == 'wind':
                install_cost += 8800 * i['size']

        for i in storage:
            install_cost += 12000 * i[0]

        return install_cost