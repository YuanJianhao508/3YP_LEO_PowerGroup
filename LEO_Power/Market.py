import pandas as pd
import numpy as np

class StorageAsset():
    def __init__(self,solar_profile, storage_profile, net_load_profile):
        self.solar_profile = solar_profile
        self.storage_profile = storage_profile
        self.net_load_profile = net_load_profile
        self.solar_cost_in = -20
        self.storage_cost_in = -20
        self.sell = 100
        self.cost = []

    def get_output(self):
        T = len(self.storage_profile)
        self.cost = np.zeros((T, 1))
        for j in range(T):
            cost = self.storage_profile * self.storage_cost_in_cost_in + self.solar_profile * self.solar_cost_in

        return self.cost

