import pandas as pd
import numpy as np

class StorageAsset():
    def __init__(self,net_load_profile, max_power, max_energy):
        self.nondispatchable_net_load = net_load_profile
        self.power_capacity = max_power
        self.energy_capacity = max_energy
        self.eff = 0.7
        self.unit_cost = 50
        self.outpute = []

    def get_output(self):
        T = len(self.nondispatchable_net_load)
        self.outpute = np.zeros((T, 1))
        soce = np.zeros((T, 1))

        for j in range(T):
            if j == 0:
                socval = self.energy_capacity
            else:
                socval = soce[j - 1]

            if self.nondispatchable_net_load[j] > 0:
                self.outpute[j] = min(self.power_capacity * 0.5, self.nondispatchable_net_load[j], self.eff * socval)
                soce[j] = socval - (1 / self.eff) * self.outpute[j]

            elif self.nondispatchable_net_load[j] < 0:
                self.outpute[j] = max(-self.power_capacity * 0.5, self.nondispatchable_net_load[j],
                                 -(1 / self.eff) * (self.energy_capacity - socval))
                soce[j] = socval - self.eff * self.outpute[j]

            elif self.nondispatchable_net_load[j] == 0:
                soce[j] = socval

        self.outpute = np.array(self.outpute).reshape(-1)
        return self.outpute


