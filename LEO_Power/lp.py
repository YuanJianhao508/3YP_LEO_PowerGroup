from EnergySystem import EnergySystem
import numpy as np
import utils
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm

plt.style.use("fivethirtyeight")  # 538样式

lp_sout = np.load('TestData/sout_lis_3.npy')
state_lis = np.load('TestData/state_lis_3.npy')
print(lp_sout)

def basic_simulation(load,solar,storage,duration):
    LEO = EnergySystem(load,solar,storage,duration)
    [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric] = LEO.simulate('all_detail')
    return [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric]

solar = [{'size':2,'type':'solarPVT'},{'size':11,'type':'solar'},{'size':5,'type':'wind'}]
load = 3500
power = 7.4
energy = 32
storage = [[power,energy,'local']]
g_labels = ['Rooftop PVT','Solar Farm PV','Wind']
s_labels = ['Local Battery']
duration = 1



length = len(lp_sout)
interval = 1440
mod = length%interval
[net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric] = basic_simulation(load,solar,storage,duration)
bas_sout = storage_profile_lis[0]['profile']

start = 270 * 48
#
# fig, ax1 = plt.subplots(figsize=(15,7))
# ax1.plot(lp_sout[start:start+48])
# ax1.plot(state_lis[start-1:start-1+48])
# ax1.plot(state_lis[start-1:start-1+48]-energy)
# ax1.plot([0.5*power for i in range(48)])
# ax1.plot([-0.5*power for i in range(48)])
# ax1.set_xlabel("Time Horizon Half-hourly Time Step")
# ax1.set_ylabel("Energy (MWh)")
# ax1.set_title('Constraint and Storage Output Decision Visualisation')
# # ax1.legend()
# plt.show()

fig, ax2 = plt.subplots(figsize=(15,7))

ax2.plot(range(48),lp_sout[start:start+48])
rect = plt.Rectangle((0,-4),48,8,fill=False,
                  edgecolor='r', linewidth=1)
ax2.add_patch(rect)
ax2.plot(range(1,49),lp_sout[start+1:start+1+48])
ax2.plot(range(2,50),lp_sout[start+2:start+2+48])
ax2.set_xlabel("xx")
ax2.set_ylabel("Energy (MWh)")
ax2.set_title('Constraint and Storage Output Decision Visualisation')
# ax1.legend()
plt.show()


