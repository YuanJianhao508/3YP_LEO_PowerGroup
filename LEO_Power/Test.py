from GenerationAsset import GenerationAsset
from Load import Load

# solar = GenerationAsset(100,2,'solar')
# solar_profile = solar.load_profile()
# print(solar_profile)
# #
myload = Load(2)

demand = myload.load_profile()
print(demand)
