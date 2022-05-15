from EnergySystem import EnergySystem
import numpy as np
import pandas as pd
import PredictiveModel as pm
import utils
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm

plt.style.use("fivethirtyeight")  # 538样式
font = {'size'   : 16}

matplotlib.rc('font', **font)

lp_sout = np.load('TestData/sout_lis_4.npy')
state_lis = np.load('TestData/state_lis_4.npy')
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

price = pd.read_csv('./Data/price.csv')
pimp_lis = np.array(price['pimp'])
pexp_lis = np.array(price['pexp'])


start = 81 * 48
#
fig, ax1 = plt.subplots(figsize=(12,9))
ax1.plot(lp_sout[start:start+48],label='Solved Storage Outputs')
ax1.plot(state_lis[start-1:start-1+48],label='State Upper Bound')
ax1.plot(state_lis[start-1:start-1+48]-energy,label='State Lower Bound')
ax1.plot([0.5*power for i in range(48)],label='Power Upper Bound')
ax1.plot([-0.5*power for i in range(48)],label='Power Lower Bound')
plt.plot(0,lp_sout[start],color='red',alpha=0.4,linestyle='--',linewidth=5,marker='o'
         ,markeredgecolor='r',markersize='15',markeredgewidth=6,label='Scheduled Current Output')
ax1.set_xlabel("Time Horizon Half-hourly Time Step")
ax1.set_ylabel("Energy (MWh)")
ax1.set_title('Constraint and Storage Output Decision Visualisation')
plt.xticks([0,6,12,18,24,30,36,42,48],['00:00','03:00','06:00','09:00','12:00','15:00','18:00','21:00','00:00'],fontsize = 'small')
ax1.legend()
plt.show()

demand = load_profile_lis[0]['profile']['Energy'].to_numpy()
g_lis_day =[]
for i in generation_profile_lis:
    k = i['profile']['Energy'].to_numpy()
    g_lis_day.append(k[start:start+48])


demand = demand[start:start+48]
solar = g_lis_day[0]+g_lis_day[1]
wind = g_lis_day[2]
raw = demand -solar-wind

plt.figure(figsize = (12,9))
plt.subplot(211)
plt.plot(raw,'--',linewidth=4, markersize=12,label='Raw Net Load')
plt.plot(solar, linewidth=2, markersize=12,label='Solar Prediction')
plt.plot(wind, linewidth=2, markersize=12,label='Wind Prediction')
plt.plot(demand,linewidth=2, markersize=12,label='Demand Prediction')

plt.xticks([0,6,12,18,24,30,36,42,48],['00:00','03:00','06:00','09:00','12:00','15:00','18:00','21:00','00:00'],fontsize = 'small')
plt.ylabel("Energy Level (MWh)")
plt.title("Predictive Constraints")
plt.legend(loc='upper right')
plt.subplot(212)
plt.plot(pimp_lis[start:start+48], linewidth=2, markersize=12,label='Export rate')
plt.plot(pexp_lis[start:start+48], linewidth=2, markersize=12,label='Import rate')
plt.xticks([0,6,12,18,24,30,36,42,48],['00:00','03:00','06:00','09:00','12:00','15:00','18:00','21:00','00:00'],fontsize = 'small')
plt.title("Energy Hub Trading Rate")
# plt.xticklabel(['00:00','03:00','06:00','09:00','12:00','15:00','18:00','21:00','00:00'],fontsize = 'small')
plt.ylabel("Trading Rates (£/MWh)")
plt.legend(loc='upper right')
plt.show()

# fig, ax2 = plt.subplots(figsize=(15,7))
# for i in range(3):
#     ax2.plot(range(0+i,48+i),lp_sout[start+i:start+i+48])
#     rect = plt.Rectangle((0+i,-4),48,8,fill=False, linewidth=1)
#     ax2.add_patch(rect)
#
# ax2.set_xlabel("xx")
# ax2.set_ylabel("Energy (MWh)")
# ax2.set_title('Constraint and Storage Output Decision Visualisation')
# # ax1.legend()
# plt.show()

