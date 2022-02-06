from mpl_toolkits import mplot3d
import Optimizer as op
from EnergySystem import EnergySystem
import numpy as np
import matplotlib.pyplot as plt

# Basic simulation


# def basic_simulation__visualization(load,solar,storage):
#     LEO = EnergySystem(load,solar,storage,5)
#     [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis] = LEO.simulate('all_detail')
#     # LEO.visualize(net_profile)
#     return [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis]
#
# solar = [{'size':18,'type':'solar'}]
# load = True
# storage = [[36,144]]
#
# # solar = [28]
# # load = True
# # storage = [[99,396]]
#
# [net_profile,load_profile_lis,generation_profile_lis,storage_profile_lis] = basic_simulation__visualization(load,solar,storage)
# load_profile = load_profile_lis[0]['Energy'].to_numpy()
# generation_profile = generation_profile_lis[0]['Energy'].to_numpy()
# net_profile = net_profile.to_numpy()
# storage_profile = storage_profile_lis[0]
# length = len(net_profile)
# mod = length%1440
#
# net_profile = net_profile[:-1195].reshape(-1,1440).sum(axis=1)
# load_profile = load_profile[:-1195].reshape(-1,1440).sum(axis=1)
# generation_profile = generation_profile[:-1195].reshape(-1,1440).sum(axis=1)
# storage_profile = storage_profile[:-1195].reshape(-1,1440).sum(axis=1)
#
# fig, ax1 = plt.subplots(figsize=(15,7))
# ax1.stackplot(np.arange(len(net_profile)), generation_profile, colors='r', alpha=0.5, labels='Generation')
# ax1.stackplot(np.arange(len(net_profile)), -storage_profile, colors='b', alpha=0.5, labels='Storage')
# ax1.stackplot(np.arange(len(net_profile)), -load_profile, colors='g', alpha=0.5, labels='Storage')
# ax1.plot(net_profile, '--r', label='Net Load')
# ax1.set_ylabel("Energy (MWh)")
# ax1.set_xlabel("Monthly period")
# ax1.set_title("Energy State of Assets over 5 years")
# ax1.legend()
# plt.show()
# # # plot breakdown of asset contribution to net load
# # fig, ax1 = plt.subplots(figsize=(15,7))
# # for asset_group, colours, types in zip(assets_by_type, asset_colours, asset_types):
# #     asset_outputs = np.array([asset.output.flatten() for asset in asset_group])
# #     ax1.stackplot(date_index, asset_outputs, colors=colours, alpha=0.5, labels=types)
# #
# # ax1.plot(net_profile, '--r', label='Net Load')
# # ax1.set_ylabel("Energy (kWh)")
# # ax1.set_xlabel("Time ")
# # ax1.set_title("Energy use by asset type")
# # ax1.set_xlim((datetime.datetime(2017,4,10), datetime.datetime(2017,4,11)))
# # ax1.legend()
# # plt.show()
#
#
# #grid search 2d test
# # #Run
# solar_ini = 0
# storage_ini = 0
# # (Solar MW Storage MW)
#
# # 4 setting
# solar_search = list(range(solar_ini, solar_ini + 60, 20))
# storage_search_power = list(range(storage_ini, storage_ini + 100, 30))
# nplis = op.grid_search_2d(solar_search,storage_search_power,load=True,duration=5)
# np.save('Result/2d_search_nplis_131.npy', nplis)
#
# nplis = np.load('Result/2d_search_nplis_131.npy')
# ta = nplis.sum(axis=2)
# money_lis = []
# pos_nplis = np.maximum(nplis, 0)
# neg_nplis = np.minimum(nplis, 0)
# pa = pos_nplis.sum(axis=2)
# na = neg_nplis.sum(axis=2)
#
#
#
# x = np.array(solar_search)
# y = np.array(storage_search_power).T
# X, Y = np.meshgrid(y, x)
#
# # print(na[3][3],pa[3][3],solar_search[3],storage_search_power[3])
# # print(X.shape,Y.shape)
# # print(pa.shape,na.shape,len(solar_search),len(storage_search_power))
# fc = np.zeros(X.shape)
# for i in range(pa.shape[0]):
#     for j in range(pa.shape[1]):
#         fc[i][j] = na[i][j] * 90 - pa[i][j] * 160 - 4400*2*solar_search[i] - 6000*2*storage_search_power[j]
#
# fc_norm = fc/np.linalg.norm(fc)
# pa_norm = -pa/np.linalg.norm(-pa)
#
# eva = 0.5*fc_norm+0.5*pa_norm
#
# plt.rcParams.update({'font.size': 12})
# fig = plt.figure(figsize=(14, 9))
# ax = plt.axes(projection='3d')
# ax.plot_surface(X,Y,fc,rstride = 1, cstride = 1,cmap='rainbow')
# ax.view_init(45,20)
# ax.set_xlabel('Storage Power Capacity (MW)')
# ax.set_ylabel('Generation Power Capacity (MW)')
# ax.set_zlabel('Normalized Financial Cost')
# ax.set_title('2D Gird Search with Integrated Financial - Energy Deficiency Metric')
#
# plt.show()
# plt.savefig('primitive_2d_grid_search.jpg')
#
#
# idx = np.unravel_index(eva.argmax(), eva.shape)
# print(X[idx],Y[idx],idx)


[generation,storage_power,storage_energy] = op.gradient_ascent()
print(generation)