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
    def __init__(self,non_dispatchable,dispatchable):
        self.non_dispatchable = non_dispatchable
        self.dispatchable = dispatchable

    def simulate(self):
        pass

    def visualize(self):
        pass

solar_farm = SolarAsset(30)
solar_panel = SolarAsset(17.5)
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
hydrogen = StorageAsset(net_nondispatchable_load,20,700)
hydrogen_profile = hydrogen.get_output()
net_nondispatchable_load = net_nondispatchable_load - hydrogen_profile

#visualize
plt.plot(net_nondispatchable_load)
plt.xlabel('Time Step')
plt.ylabel('Net Load (Energy Level)')
plt.title('Simulation Sample Data')
plt.savefig('e4.png')
plt.show()

