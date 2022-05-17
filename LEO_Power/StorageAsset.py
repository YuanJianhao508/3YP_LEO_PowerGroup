import matplotlib.pyplot as plt
import numpy as np

class StorageAsset():
    def __init__(self,net_load_profile, max_power, max_energy, type):
        self.nondispatchable_net_load = net_load_profile
        self.power_capacity = max_power
        self.energy_capacity = max_energy
        self.type = type
        self.eff_dict = {'local':0.7,'hydrogen':0.5}
        self.eff = 0
        self.outpute = []

    def get_output(self):
        #Positive output means energy flows out from battery
        self.eff = self.eff_dict[self.type]
        T = len(self.nondispatchable_net_load)
        self.outpute = np.zeros((T, 1))
        soce = np.zeros((T, 1))

        for j in range(T):
            if j == 0:
                # socval = self.energy_capacity
                socval = 0
            else:
                socval = soce[j - 1]

            if self.nondispatchable_net_load[j] > 0:
                self.outpute[j] = min(self.power_capacity * 0.5, self.nondispatchable_net_load[j], self.eff * socval)
                soce[j] = socval - (1 / self.eff) * self.outpute[j]

            elif self.nondispatchable_net_load[j] < 0:
                self.outpute[j] = max(-self.power_capacity * 0.5, self.nondispatchable_net_load[j],
                                 - (1 / self.eff) * (self.energy_capacity - socval))
                soce[j] = socval - self.eff * self.outpute[j]

            elif self.nondispatchable_net_load[j] == 0:
                soce[j] = socval



        self.outpute = np.array(self.outpute).reshape(-1)

        return self.outpute

    def get_smart_output(self):
        lp_sout = 1.5*np.load('TestData/sout_lis.npy')
        return lp_sout


    # def linprog(settings,start,duration=1):
    #     generation = settings[0]
    #     load = settings[1]
    #     storage = settings[2]
    #     window = 336
    #     LEO = EnergySystem(load, generation, storage, duration)
    #     [net_profile, load_profile_lis, generation_profile_lis, storage_profile_lis, metric] = LEO.simulate('all_detail')
    #     g_lis_window = []
    #     for i in generation_profile_lis:
    #         k = i['profile']['Energy'].to_numpy()
    #         g_lis_window.append(k[start:start+window])

