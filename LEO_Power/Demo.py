from mpl_toolkits import mplot3d
import Optimizer as op
from EnergySystem import EnergySystem
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# # Basic simulation
# def basic_simulation__visualization(load,solar,storage):
#     LEO = EnergySystem(load,solar,storage,5)
#     net_profile = LEO.simulate()
#     LEO.visualize(net_profile)
#     return net_profile
#
# solar = [25,25]
# load = True
# storage = [[15,200],[15,5000]]
# net_profile = basic_simulation__visualization(load,solar,storage)
# print(sum(net_profile))


#grid search 2d test
# #Run
solar_ini = 0
storage_ini = 0
# (Solar MW Storage MW)

# 4 setting
solar_search = list(range(solar_ini, solar_ini + 60, 2))
storage_search_power = list(range(storage_ini, storage_ini + 100, 3))
nplis = op.grid_search_2d(solar_search,storage_search_power,load=True,duration=1)
np.save('Result/2d_search_nplis_129.npy', nplis)

nplis = np.load('Result/2d_search_nplis_129.npy')
ta = nplis.sum(axis=2)
money_lis = []
pos_nplis = np.maximum(nplis, 0)
neg_nplis = np.minimum(nplis, 0)
pa = pos_nplis.sum(axis=2)
na = neg_nplis.sum(axis=2)



x = np.array(solar_search)
y = np.array(storage_search_power).T
X, Y = np.meshgrid(y, x)

# print(na[3][3],pa[3][3],solar_search[3],storage_search_power[3])
# print(X.shape,Y.shape)
# print(pa.shape,na.shape,len(solar_search),len(storage_search_power))
fc = np.zeros(X.shape)
for i in range(pa.shape[0]):
    for j in range(pa.shape[1]):
        fc[i][j] = na[i][j] * 90 - pa[i][j] * 100 - 4400*solar_search[i] - 1200*storage_search_power[j]

gna = (pa*0.8+na*0.2)
inm = (gna/gna.mean() + fc/fc.mean())

fig = plt.figure(figsize=(14, 9))
ax = plt.axes(projection='3d')
ax.plot_surface(X,Y,fc,rstride = 1, cstride = 1,cmap='rainbow')
ax.view_init(45,20)
ax.set_xlabel('Storage Power Capacity (MW)')
ax.set_ylabel('Generation Power Capacity (MW)')
ax.set_zlabel('Cost Function: Financial Cost')
plt.show()
plt.savefig('primitive_2d_grid_search.jpg')
