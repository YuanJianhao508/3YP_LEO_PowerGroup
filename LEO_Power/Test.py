from SolarAsset import SolarAsset
from Load import Load

# solar = SolarAsset(100,1)
# solar_profile = solar.load_profile()
# print(solar_profile)
# #
myload = Load(1)

demand = myload.load_profile()
print(demand)
