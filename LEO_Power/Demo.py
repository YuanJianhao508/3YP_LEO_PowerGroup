from mpl_toolkits import mplot3d
import Optimizer as op
from EnergySystem import EnergySystem
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import utils

plt.style.use("fivethirtyeight")  # 538样式
# plt.savefig('books_read.png')

# Basic simulation

def basic_simulation(load,solar,storage,duration):
    LEO = EnergySystem(load,solar,storage,duration)
    [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric] = LEO.simulate('all_detail')
    return [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric]

#Version1
# solar = [{'size':17.5,'type':'solar'},{'size':20,'type':'solar'}]
# load = 3500
# storage = [[2,15,'local'],[10,5000,'hydrogen']]
# g_labels = ['Rooftop Solar','Solar Farm']
# s_labels = ['Local Battery','Hydrogen']
# duration = 5

# SGD
solar = [{'size':2,'type':'solarPVT'},{'size':11,'type':'solar'},{'size':5,'type':'wind'}]
load = 3500
storage = [[7.4,32,'local']]
g_labels = ['Rooftop PVT','Solar Farm PV','Wind']
s_labels = ['Local Battery']
duration = 1

#GS
# solar = [{'size':2,'type':'solarPVT'},{'size':10,'type':'solar'},{'size':5,'type':'wind'}]
# load = 3500
# storage = [[4,40,'local']]
# g_labels = ['PVT','PV','Wind']
# s_labels = ['Local Battery']
# duration = 1

[net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis,metric] = basic_simulation(load,solar,storage,duration)

load_profile = load_profile_lis[0]['profile']['Energy'].to_numpy()
net_profile = net_profile.to_numpy()
length = len(net_profile)
interval = 1440
mod = length%interval
#
#
#
# Long-term Vis
# g_lis =[]
# for i in generation_profile_lis:
#     # print(i)
#     k = i['profile']['Energy'].to_numpy()
#     # print(k)
#     g_lis.append(k[:-mod].reshape(-1,interval).sum(axis=1))
# s_lis = []
# for i in storage_profile_lis:
#     k = -i['profile']
#     s_lis.append(k[:-mod].reshape(-1,interval).sum(axis=1))
#
#
#
#
# net_profile_year = net_profile[:-mod].reshape(-1,interval).sum(axis=1)
# load_profile_year = load_profile[:-mod].reshape(-1,interval).sum(axis=1)
#
#
# # print(load_profile_year)
#
# date_index = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']
#
# # date_index = np.arange(60)
#
#
# pv_colourmap = cm.get_cmap("Wistia")
# load_colourmap = cm.get_cmap('copper')
# bat_colourmap = cm.get_cmap('winter')
# g_color = pv_colourmap(range(0,256,int(np.ceil(256/len(solar)))))
# l_color = load_colourmap(range(0,256,int(np.ceil(256/1))))
# s_color = bat_colourmap(range(0,256,int(np.ceil(256/len(storage)))))
#
#
# # plot breakdown of asset contribution to net load
# fig, ax1 = plt.subplots(figsize=(15,7))
# ax1.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)
# ax1.stackplot(date_index, g_lis, colors=g_color, alpha=0.5, labels=g_labels)
# ax1.stackplot(date_index, load_profile_year, colors=l_color, alpha=0.5, labels=['Demand Load'])
# ax1.stackplot(date_index, s_lis, colors=s_color, alpha=0.5, labels=s_labels)
#
# ax1.plot(net_profile_year, '--r', label='Net Load')
# ax1.set_ylabel("Energy (MWh)")
# ax1.set_xlabel("Monthly period")
# ax1.set_title("Energy State of Assets over Five Years")
# ax1.legend()
# plt.show()

#
#
# Short Term Vis
# winter
start = 48*350
day = 48
net_profile_day = net_profile[start:start+day]
load_profile_day = load_profile[start:start+day]
g_lis_day =[]
for i in generation_profile_lis:
    k = i['profile']['Energy'].to_numpy()
    g_lis_day.append(k[start:start+day])
s_lis_day = []
for i in storage_profile_lis:
    k = i['profile']
    s_lis_day.append(k[start:start+day])

date_index = np.arange(48)
pv_colourmap = cm.get_cmap("Wistia")
load_colourmap = cm.get_cmap('copper')
bat_colourmap = cm.get_cmap('winter')
g_color = pv_colourmap(range(0,256,int(np.ceil(256/len(solar)))))
l_color = load_colourmap(range(0,256,int(np.ceil(256/1))))
s_color = bat_colourmap(range(0,256,int(np.ceil(256/len(storage)))))
fig, ax2 = plt.subplots(figsize=(15,7))
ax2.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)
ax2.stackplot(date_index, g_lis_day, colors=g_color, alpha=0.5, labels=g_labels)
ax2.stackplot(date_index, load_profile_day, colors=l_color, alpha=0.5, labels=['Demand Load'])
ax2.stackplot(date_index, s_lis_day, colors=s_color, alpha=0.5, labels=s_labels)
ax2.plot(net_profile_day, '--r', label='Net Load')
ax2.set_xticks([0,6,12,18,24,30,36,42,48])
ax2.set_xticklabels(['00:00','03:00','06:00','09:00','12:00','15:00','18:00','21:00','00:00'],fontsize = 'small')
ax2.set_ylabel("Energy (MWh)")
ax2.set_xlabel("Half-hourly period")
ax2.set_title("Energy State of Assets over a Typical Summer Day")
ax2.legend()
plt.show()







# grid search 2d test
#
# solar_ini = 0
# wind_ini = 0
# storage_ini = 2
# # (Solar MW Storage MW)
#
# # 4 setting
# solar_search = list(range(solar_ini, solar_ini + 50, 2))
# wind_search = list(range(wind_ini, wind_ini + 6, 1))
# storage_search = list(range(storage_ini, storage_ini + 20, 2))
# # net_loads,net_costs = op.GridSearch(solar_search,wind_search,storage_search)
# # #
# # np.save('net_cost2',net_costs)
# net_costs = np.load('net_cost2.npy')
#
# fig, ax = plt.subplots(figsize=(15,7))
# ax.plot(range(solar_ini, solar_ini + 50, 2), net_costs[:,5,:])
# ax.set_xlabel("Solar Panel Power Capacity (MW)")
# ax.set_ylabel("Annual Integrated System Cost (£)")
# ax.legend(labels=range(storage_ini, storage_ini + 20, 2), loc=4, title="Battery Power Capacity (MW)")
# #ax.set_ybound(0)
# plt.show()
#
# fig, ax1 = plt.subplots(figsize=(15,7))
# ax1.plot(range(wind_ini, wind_ini + 6, 1), net_costs[0,:,:])
# ax1.set_xlabel("No. of Wind Turbines")
# ax1.set_ylabel("Annual Integrated System Cost (£)")
# ax1.legend(labels=range(storage_ini, storage_ini + 20, 2), loc=1, title="Battery Power Capacity (MW)")
# #ax.set_ybound(0)
# plt.show()
#
# print(net_costs.min(),net_costs.argmin())
# index = np.where(net_costs==net_costs.max())
# print(index)
# print(solar_search[index[0][0]],wind_search[index[1][0]],storage_search[index[2][0]])
# print(net_costs[0,0,9])


# SGD
# solar = [{'size':37.5,'type':'solar'},{'size':0,'type':'wind'}]
# load = 3500
# storage = [[20,80,'local']]
#
# theta = [solar,storage]
#
# gl, sl, log = op.SGD(theta)
# solar_log = []
# wind_log = []
# for i in gl:
#     solar_log.append(i[0]['size'])
#     wind_log.append(i[1]['size']*2)
# solar_log = np.array(solar_log)
# wind_log = np.array(wind_log)
# np.save('TestData/solar_log1',solar_log)
# np.save('TestData/wind_log1',wind_log)
# sp_log = []
# se_log = []
# for i in sl:
#     sp_log.append(i[0][0])
#     se_log.append(i[0][1])
# sp_log=np.array(sp_log)
# se_log=np.array(se_log)
# np.save('TestData/sp_log1',sp_log)
# np.save('TestData/se_log1',se_log)
# res = np.array(log)
# np.save('TestData/log1',res)
#
#
# res = np.load('TestData/log1.npy')
# solar_log = np.load('TestData/solar_log1.npy')
# wind_log = np.load('TestData/wind_log1.npy')
# sp_log = np.load('TestData/sp_log1.npy')
# se_log = np.load('TestData/se_log1.npy')
#
# print(solar_log[-1],wind_log[-1],se_log[-1],sp_log[-1])
# fig, ax1 = plt.subplots(figsize=(15,7))
# ax1.plot(res,label='Integrated System Cost')
# ax1.set_xlabel("No. Iteration")
# ax1.set_ylabel("Annual Integrated System Cost (£)")
# ax1.set_title('Training Cost Function')
# plt.legend()
# plt.show()
#
#
# plt.figure(figsize = (15, 7))
# plt.subplot(211)
# plt.plot(solar_log, linewidth=2, markersize=12,label='Solar')
# plt.plot(wind_log, linewidth=2, markersize=12,label='Wind')
# plt.plot(sp_log, linewidth=2, markersize=12,label='Storage')
# plt.ylabel("Power Capacity (MW)")
# plt.title("Training Asset Size")
# plt.legend()
# plt.subplot(212)
# plt.plot(se_log, linewidth=2, markersize=12,label='Storage')
# plt.xlabel("No.Iteration")
# plt.ylabel("Energy Capacity (MWh)")
# plt.legend()
# plt.show()

