from GenerationAsset import GenerationAsset
from Load import Load
from EnergySystem import EnergySystem

# solar = GenerationAsset(100,2,'solar')
# solar_profile = solar.load_profile()
# print(solar_profile)
#


# myload = Load(2)
# demand = myload.load_profile()
# print(demand)

solar = [{'size':30,'type':'solar'}]
load = True
storage = [[16,120]]
LEO = EnergySystem(load,solar,storage,5)
[net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric] = LEO.simulate('all_detail')
print(metric)