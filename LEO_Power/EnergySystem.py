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

my_solar_farm = SolarAsset(10000)
# get solar profile
solar_profile = my_solar_farm.load_profile()

# get demand profile
my_load = Load()
load_profile = my_load.load_profile()


#get ned load and feed to storage
net_nondispatchable_load = load_profile - solar_profile
# net_nondispatchable_load = net_nondispatchable_load

#get storage output
my_storage = StorageAsset(net_nondispatchable_load,10000,50000)
storage_profile = my_storage.get_output().reshape(-1)
storage_profile = pd.Series(storage_profile)

#calculate net load
net_load = net_nondispatchable_load - storage_profile

#market model
# my_market = Market(solar_profile,storage_profile,net_load)
# cost =
#visualize
plt.plot(net_load)
plt.xlabel('Time Step')
plt.ylabel('Net Load (Energy Level)')
plt.title('Simulation Sample Data')
plt.savefig('e2.png')
plt.show()

