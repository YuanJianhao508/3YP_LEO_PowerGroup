import pandas as pd
import matplotlib.pyplot as plt
from SolarAsset import SolarAsset
from Load import Load
from StorageAsset import StorageAsset


# We want
# 1. Solar/load energy profile daily/half_hourly
# 2. Solar/load power profile daily/half_hourly
# With this two profile, we want
# 3. Calculate required power/energy profile from storage, based on design feature
# 4. simulate the whole system power/energy/cost and optimize
class EnergySystem():
    def __init__(self,load,solar,storage):
        self.load = load
        self.solar = solar
        self.dispatchable = storage

    def simulate(self):
        # load profile
        load = Load()
        load_profile = load.load_profile()

        # solar profile


        for k,i in enumerate(self.solar):
            generation = SolarAsset(i)
            if k == 0:
                generation_profile = generation.load_profile()
            else:
                generation_profile += generation.load_profile()


        #dispatchable -- battery

        net_nondispatchable_load = load_profile['Energy'] - generation_profile['Energy']
        for k,i in enumerate(self.dispatchable):
            storage = StorageAsset(net_nondispatchable_load, i[0], i[1])
            storage_profile = storage.get_output()
            net_nondispatchable_load = net_nondispatchable_load - storage_profile

        return net_nondispatchable_load

    def visualize(self,net_nondispatchable_load):
        plt.plot(net_nondispatchable_load)
        plt.xlabel('Time Step')
        plt.ylabel('Net Load (Energy Level)')
        plt.title('Simulation Sample Data')
        # plt.savefig('e4.png')
        plt.show()

solar = [30,17.5]
load = True
storage = [[7.5,20],[7.5,20]]

LEO = EnergySystem(load,solar,storage)
net_profile = LEO.simulate()
LEO.visualize(net_profile)

# solar_farm = SolarAsset(30)
# solar_panel = SolarAsset(17.5)
#
# solar_profile = solar_farm.load_profile()+solar_panel.load_profile()
#
# # get demand profile
# load = Load()
# load_profile = load.load_profile()
#
#
# #get ned load and feed to storage
# net_nondispatchable_load = load_profile['Energy'] - solar_profile['Energy']
#
#
# #get storage output
# local_battery = StorageAsset(net_nondispatchable_load,7.5,20)
# local_battery_profile = local_battery.get_output()
#
# net_nondispatchable_load = net_nondispatchable_load - local_battery_profile
# hydrogen = StorageAsset(net_nondispatchable_load,7.5,20)
# hydrogen_profile = hydrogen.get_output()
# net_nondispatchable_load = net_nondispatchable_load - hydrogen_profile
#
# #visualize
# plt.plot(net_nondispatchable_load)
# plt.xlabel('Time Step')
# plt.ylabel('Net Load (Energy Level)')
# plt.title('Simulation Sample Data')
# plt.savefig('e4.png')
# plt.show()

